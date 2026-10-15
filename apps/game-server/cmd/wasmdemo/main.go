//go:build js && wasm

// wasmdemo biên dịch server game THẬT (engine, catalog, luật) sang WebAssembly để chạy ngay trong trình duyệt,
// dùng cho bản thử trên điện thoại khi chưa có server. Kho dữ liệu trong bộ nhớ: tắt trang là mất.
// Không dùng cho sản xuất. Dữ liệu catalog được go:embed từ thư mục data/ (xem tools/build-wasm-demo.sh).
package main

import (
	"context"
	"embed"
	"io/fs"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"phimond/server/internal/devstore"
	"phimond/server/internal/transport"
	"strconv"
	"syscall/js"
)

//go:embed all:data
var dataFS embed.FS

func main() {
	sub, err := fs.Sub(dataFS, "data")
	if err != nil {
		panic(err)
	}
	catalog, err := content.LoadFS(sub)
	if err != nil {
		panic(err)
	}
	srv := transport.New(devstore.New(), character.NewEngine(catalog))
	conns := map[string]*transport.LocalConn{}
	next := 0
	api := map[string]any{
		// http(method, path, bodyJSON|"", token) -> {status, body}
		"http": js.FuncOf(func(_ js.Value, a []js.Value) any {
			var body []byte
			if a[2].String() != "" {
				body = []byte(a[2].String())
			}
			code, out := srv.LocalHTTP(a[0].String(), a[1].String(), body, a[3].String())
			return map[string]any{"status": code, "body": string(out)}
		}),
		// open() -> connId
		"open": js.FuncOf(func(_ js.Value, _ []js.Value) any {
			next++
			id := strconv.Itoa(next)
			conns[id] = srv.NewLocalConn()
			return id
		}),
		// send(connId, frameJSON) -> {out, closed}
		"send": js.FuncOf(func(_ js.Value, a []js.Value) any {
			c := conns[a[0].String()]
			if c == nil {
				return map[string]any{"out": "", "closed": true}
			}
			out, closed := c.Handle(context.Background(), []byte(a[1].String()))
			if closed {
				delete(conns, a[0].String())
			}
			return map[string]any{"out": string(out), "closed": closed}
		}),
		"close": js.FuncOf(func(_ js.Value, a []js.Value) any { delete(conns, a[0].String()); return nil }),
	}
	js.Global().Set("phimondEngine", js.ValueOf(api))
	js.Global().Set("phimondEngineReady", true)
	select {}
}
