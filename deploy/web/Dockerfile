# Phimond web: build client (Vite) rồi phục vụ bằng nginx không cần quyền root.
# Context = gốc repo. Chạy: docker build -f deploy/web/Dockerfile -t phimond-web .
FROM node:20-alpine AS build
WORKDIR /repo
COPY packages/protocol-ts packages/protocol-ts
COPY apps/client apps/client
WORKDIR /repo/apps/client
RUN npm ci --no-audit --no-fund
# VITE_GAME_API_URL để trống: client gọi cùng origin (/api, /ws) qua Ingress.
RUN npm run build \
 && find dist -name '*.map' -delete
# Harbor nằm sau Cloudflare: mỗi request (mỗi layer khi push) phải < 100 MB, quá là bị 413 Payload Too Large
# (lỗi CI v1.1.1, 2026-11-18). Bản build được chép thành nhiều layer bên dưới; chặn ngay ở đây nếu một phần vượt 90 MB.
RUN for d in hd2d ui battle pets audio; do \
      s=$(du -sm "dist/$d" | cut -f1); echo "dist/$d: ${s} MB"; \
      if [ "$s" -gt 90 ]; then echo "dist/$d ${s} MB > 90 MB: layer sẽ bị Cloudflare chặn (413). Tách thêm COPY hoặc giảm ảnh." >&2; exit 1; fi; \
    done \
 && mkdir -p /out/rest \
 && cd dist && for f in *; do case "$f" in hd2d|ui|battle|pets|audio) ;; *) cp -r "$f" /out/rest/ ;; esac; done

FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY deploy/web/nginx.conf /etc/nginx/conf.d/default.conf
# Mỗi thư mục asset một layer (< 100 MB mỗi layer, xem trên). Thứ tự: thư mục ít đổi trước để tận dụng cache layer.
COPY --from=build /repo/apps/client/dist/audio /usr/share/nginx/html/audio
COPY --from=build /repo/apps/client/dist/pets /usr/share/nginx/html/pets
COPY --from=build /repo/apps/client/dist/battle /usr/share/nginx/html/battle
COPY --from=build /repo/apps/client/dist/ui /usr/share/nginx/html/ui
COPY --from=build /repo/apps/client/dist/hd2d /usr/share/nginx/html/hd2d
COPY --from=build /out/rest /usr/share/nginx/html
EXPOSE 8080
