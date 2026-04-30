# Index Optimization Notes

## General Guidelines
- Primary keys are automatically indexed
- Add indexes to columns used in WHERE clauses
- Add indexes to foreign key columns
- Use composite indexes for multi-column queries
- Monitor query performance with EXPLAIN QUERY PLAN

## SQLite-Specific
- SQLite uses B-tree indexes by default
- VACUUM periodically to reclaim space
- Use WAL mode for concurrent reads: PRAGMA journal_mode=WAL
