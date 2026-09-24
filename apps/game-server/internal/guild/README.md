# internal/guild

Guild system — implements spec §38. TBD.

Will host guild create / invite / accept / leave / promote / kick flows,
guild chat delegation to `internal/chat`, and the wire namespace
`guild.*` declared in spec §50.

> Spec §38 explicitly states "Không cần hoàn thiện guild endgame ngay
> trong vertical slice" — full endgame progression can wait.