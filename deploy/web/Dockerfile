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

FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY deploy/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /repo/apps/client/dist /usr/share/nginx/html
EXPOSE 8080
