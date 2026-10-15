package transport

import (
	"net/http"
	"strings"
)

// CORS cho client game web chạy ở origin khác (vd. Vite dev server).
// Mặc định tắt: chỉ bật khi GAME_CORS_ORIGINS liệt kê origin đầy đủ (scheme://host[:port]),
// phân tách bằng dấu phẩy. Không hỗ trợ ký tự đại diện. Token đi trong header Authorization,
// không dùng cookie, nên không bật Allow-Credentials.

func parseCORSOrigins(v string) map[string]bool {
	out := map[string]bool{}
	for _, o := range strings.Split(v, ",") {
		o = strings.TrimSpace(o)
		if o == "" || o == "*" || strings.HasSuffix(o, "/") || !strings.Contains(o, "://") {
			continue
		}
		out[o] = true
	}
	return out
}

// applyCORS gắn header cho origin hợp lệ. Trả true nếu request là preflight đã được xử lý xong.
func (s *Server) applyCORS(w http.ResponseWriter, r *http.Request) bool {
	origin := r.Header.Get("Origin")
	if origin == "" || len(s.cors) == 0 {
		return false
	}
	h := w.Header()
	h.Add("Vary", "Origin")
	allowed := s.cors[origin]
	preflight := r.Method == http.MethodOptions && r.Header.Get("Access-Control-Request-Method") != ""
	if !allowed {
		if preflight {
			fail(w, http.StatusForbidden, "origin not allowed")
			return true
		}
		return false
	}
	h.Set("Access-Control-Allow-Origin", origin)
	if preflight {
		h.Add("Vary", "Access-Control-Request-Method")
		h.Add("Vary", "Access-Control-Request-Headers")
		h.Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		h.Set("Access-Control-Allow-Headers", "Authorization, Content-Type")
		h.Set("Access-Control-Max-Age", "600")
		w.WriteHeader(http.StatusNoContent)
		return true
	}
	return false
}
