# Testing results

Function | SQLite3 | MongoDB
-----|-----|-----
Load user CSV | 252ms | 2.45s
Load status CSV | 64.3s | 458s
Add user | 3ms | 20 ms
Update user | 2ms | 3ms
Search user | 1ms | 1ms
Delete user | 3ms | 4ms
Add status | 1ms | 1ms
Update status | 2ms | 3ms
Search status | 1ms | 1ms
Delete status | 1ms | 1ms

# Notes
My MongoDB backed code is a lot slower. This is likely because MongoDB doesn't have any checks for me,
so I have to check everything myself. Sqlite has opitmized their algorithms to do these checks when
I have not.

# Conclusion
If performance is key Sqlite would be the way to go. Our data has clear relationships that MongoDB
can't handle as well as Sqlite, leading to performance problems.
