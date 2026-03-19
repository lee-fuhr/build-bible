#!/usr/bin/env python3
"""
Build Bible FTS5 indexer.

Parses Build Bible.md into sections, stores in SQLite with FTS5 for instant
full-text search by any hook. Same tech pattern as sessions.db.

Usage:
    python3 bible_index.py --reindex       # Force rebuild from Build Bible.md
    python3 bible_index.py --search "TDD"  # Quick CLI search test

Database: bible.db (same directory as this script)
Source: Work/_ Infrastructure/Build Bible.md
"""

import sys
import os
import re
import sqlite3
from pathlib import Path

BIBLE_PATH = Path(os.environ.get("BIBLE_PATH", "Build Bible.md"))
DB_PATH = Path(__file__).resolve().parent / "bible.db"


def get_db() -> sqlite3.Connection:
    """Get connection, creating schema if needed."""
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA journal_mode=WAL")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS bible_sections (
            id INTEGER PRIMARY KEY,
            section_number TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            line_start INTEGER,
            line_end INTEGER,
            parent_section TEXT
        );

        CREATE TABLE IF NOT EXISTS bible_meta (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    """)
    # Check if FTS table exists
    row = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bible_fts'"
    ).fetchone()
    if not row:
        db.executescript("""
            CREATE VIRTUAL TABLE bible_fts USING fts5(
                section_number, title, content,
                content=bible_sections, content_rowid=id
            );

            CREATE TRIGGER IF NOT EXISTS bible_sections_ai AFTER INSERT ON bible_sections BEGIN
                INSERT INTO bible_fts(rowid, section_number, title, content)
                VALUES (new.id, new.section_number, new.title, new.content);
            END;

            CREATE TRIGGER IF NOT EXISTS bible_sections_ad AFTER DELETE ON bible_sections BEGIN
                INSERT INTO bible_fts(bible_fts, rowid, section_number, title, content)
                VALUES ('delete', old.id, old.section_number, old.title, old.content);
            END;

            CREATE TRIGGER IF NOT EXISTS bible_sections_au AFTER UPDATE ON bible_sections BEGIN
                INSERT INTO bible_fts(bible_fts, rowid, section_number, title, content)
                VALUES ('delete', old.id, old.section_number, old.title, old.content);
                INSERT INTO bible_fts(rowid, section_number, title, content)
                VALUES (new.id, new.section_number, new.title, new.content);
            END;
        """)
    return db


def parse_bible(bible_path: Path) -> list[dict]:
    """Parse Build Bible.md into sections by ## and ### headings."""
    text = bible_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    sections = []
    current = None
    # Regex for headings: ## 1. Core principles or ### 1.3 Test first...
    heading_re = re.compile(r'^(#{2,3})\s+(.+)$')
    # Extract section number from heading text
    number_re = re.compile(r'^(\d+(?:\.\d+)*)')

    for i, line in enumerate(lines, start=1):
        m = heading_re.match(line)
        if m:
            # Close previous section
            if current:
                current["line_end"] = i - 1
                current["content"] = "\n".join(
                    lines[current["line_start"] - 1 : i - 1]
                ).strip()
                sections.append(current)

            level = len(m.group(1))  # 2 for ##, 3 for ###
            title_text = m.group(2).strip()

            # Extract section number
            num_match = number_re.match(title_text)
            if num_match:
                section_number = num_match.group(1)
            else:
                # Headings without numbers (e.g., "Principle interaction model")
                # Use parent section + title slug
                section_number = title_text.lower().replace(" ", "-")[:30]

            # Determine parent
            parent = None
            if level == 3 and section_number and "." in section_number:
                parent = section_number.split(".")[0]
            elif level == 3:
                # Find last ## section
                for s in reversed(sections):
                    if s.get("_level") == 2:
                        parent = s["section_number"]
                        break

            current = {
                "section_number": section_number,
                "title": title_text,
                "line_start": i,
                "line_end": None,
                "content": "",
                "parent_section": parent,
                "_level": level,
            }

    # Close last section
    if current:
        current["line_end"] = len(lines)
        current["content"] = "\n".join(
            lines[current["line_start"] - 1 :]
        ).strip()
        sections.append(current)

    return sections


def reindex(db: sqlite3.Connection | None = None) -> int:
    """Rebuild the FTS5 index from Build Bible.md. Returns section count."""
    if not BIBLE_PATH.exists():
        print(f"Bible not found at {BIBLE_PATH}", file=sys.stderr)
        return 0

    close_db = db is None
    if db is None:
        db = get_db()

    sections = parse_bible(BIBLE_PATH)

    # Clear and rebuild
    db.execute("DELETE FROM bible_sections")
    # Rebuild FTS
    db.execute("INSERT INTO bible_fts(bible_fts) VALUES ('rebuild')")

    for s in sections:
        db.execute(
            """INSERT INTO bible_sections
               (section_number, title, content, line_start, line_end, parent_section)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                s["section_number"],
                s["title"],
                s["content"],
                s["line_start"],
                s["line_end"],
                s["parent_section"],
            ),
        )

    # Store metadata
    import hashlib
    bible_hash = hashlib.md5(BIBLE_PATH.read_bytes()).hexdigest()
    db.execute(
        "INSERT OR REPLACE INTO bible_meta (key, value) VALUES ('bible_hash', ?)",
        (bible_hash,),
    )
    db.execute(
        "INSERT OR REPLACE INTO bible_meta (key, value) VALUES ('section_count', ?)",
        (str(len(sections)),),
    )

    db.commit()
    if close_db:
        db.close()
    return len(sections)


def needs_reindex() -> bool:
    """Check if Bible has changed since last index."""
    if not DB_PATH.exists():
        return True
    if not BIBLE_PATH.exists():
        return False

    import hashlib
    current_hash = hashlib.md5(BIBLE_PATH.read_bytes()).hexdigest()

    db = get_db()
    row = db.execute(
        "SELECT value FROM bible_meta WHERE key='bible_hash'"
    ).fetchone()
    db.close()

    if not row:
        return True
    return row[0] != current_hash


def search_bible(query: str, limit: int = 3) -> list[dict]:
    """FTS5 search -> top N sections with snippets and scores.

    Returns: [{"section": "1.3", "title": "...", "snippet": "...", "score": -12.5}]
    """
    if not DB_PATH.exists():
        # Auto-index on first search
        count = reindex()
        if count == 0:
            return []

    if needs_reindex():
        reindex()

    db = get_db()
    try:
        rows = db.execute(
            """SELECT
                   s.section_number,
                   s.title,
                   snippet(bible_fts, 2, '>>>', '<<<', '...', 40) as snippet,
                   bm25(bible_fts) as score
               FROM bible_fts
               JOIN bible_sections s ON s.id = bible_fts.rowid
               WHERE bible_fts MATCH ?
               ORDER BY score
               LIMIT ?""",
            (query, limit),
        ).fetchall()

        return [
            {
                "section": row[0],
                "title": row[1],
                "snippet": row[2],
                "score": row[3],
            }
            for row in rows
        ]
    except sqlite3.OperationalError:
        # Bad FTS query syntax — try wrapping terms
        try:
            safe_query = " OR ".join(
                f'"{w}"' for w in query.split() if len(w) > 2
            )
            if not safe_query:
                return []
            rows = db.execute(
                """SELECT
                       s.section_number,
                       s.title,
                       snippet(bible_fts, 2, '>>>', '<<<', '...', 40) as snippet,
                       bm25(bible_fts) as score
                   FROM bible_fts
                   JOIN bible_sections s ON s.id = bible_fts.rowid
                   WHERE bible_fts MATCH ?
                   ORDER BY score
                   LIMIT ?""",
                (safe_query, limit),
            ).fetchall()
            return [
                {
                    "section": row[0],
                    "title": row[1],
                    "snippet": row[2],
                    "score": row[3],
                }
                for row in rows
            ]
        except sqlite3.OperationalError:
            return []
    finally:
        db.close()


def get_section_content(section_number: str) -> str | None:
    """Get full content of a section by number."""
    if not DB_PATH.exists():
        return None

    db = get_db()
    row = db.execute(
        "SELECT content FROM bible_sections WHERE section_number = ?",
        (section_number,),
    ).fetchone()
    db.close()

    return row[0] if row else None


def get_section_with_children(section_number: str) -> str | None:
    """Get full content of a top-level section including all subsections."""
    if not DB_PATH.exists():
        return None

    db = get_db()
    # Get the section itself + all children (e.g., "6" gets "6", "6.1", "6.2", etc.)
    rows = db.execute(
        """SELECT content FROM bible_sections
           WHERE section_number = ? OR parent_section = ?
           ORDER BY line_start""",
        (section_number, section_number),
    ).fetchall()
    db.close()

    if not rows:
        return None
    return "\n\n".join(r[0] for r in rows)


def get_sections_by_numbers(numbers: list[str]) -> list[dict]:
    """Get multiple sections by their numbers."""
    if not DB_PATH.exists():
        return []

    db = get_db()
    placeholders = ",".join("?" for _ in numbers)
    rows = db.execute(
        f"""SELECT section_number, title, content
            FROM bible_sections
            WHERE section_number IN ({placeholders})
            ORDER BY line_start""",
        numbers,
    ).fetchall()
    db.close()

    return [
        {"section": r[0], "title": r[1], "content": r[2]}
        for r in rows
    ]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build Bible FTS5 indexer")
    parser.add_argument("--reindex", action="store_true", help="Force rebuild index")
    parser.add_argument("--search", type=str, help="Search the Bible")
    parser.add_argument("--limit", type=int, default=3, help="Max results")
    parser.add_argument("--section", type=str, help="Get section content by number")
    args = parser.parse_args()

    if args.reindex:
        count = reindex()
        print(f"Indexed {count} sections from {BIBLE_PATH}")
    elif args.search:
        results = search_bible(args.search, limit=args.limit)
        if not results:
            print("No results.")
        for r in results:
            print(f"  [{r['section']}] {r['title']} (score: {r['score']:.1f})")
            print(f"    {r['snippet']}")
            print()
    elif args.section:
        content = get_section_content(args.section)
        if content:
            print(content)
        else:
            print(f"Section {args.section} not found.")
    else:
        # Default: check if reindex needed
        if needs_reindex():
            count = reindex()
            print(f"Auto-indexed {count} sections (Bible changed)")
        else:
            db = get_db()
            row = db.execute(
                "SELECT value FROM bible_meta WHERE key='section_count'"
            ).fetchone()
            db.close()
            print(f"Index up-to-date ({row[0] if row else '?'} sections)")
