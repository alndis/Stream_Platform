# Используем образ Node.js в качестве базового для создания фронтенд-приложения
FROM node:18 AS build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json (если есть) для установки зависимостей
COPY package*.json ./

# Устанавливаем зависимости для приложения
RUN npm install

# Создаем проект на Vite (если он не был создан локально)
RUN npm create vite@latest . -- --template react

# Устанавливаем дополнительные зависимости, такие как TailwindCSS, Ant Design, Axios, и другие
RUN npm install -D tailwindcss postcss autoprefixer && \
    npm install tailwindcss init -p && \
    npm install antd axios prop-types

# Копируем все файлы приложения в контейнер
COPY . .

# Собираем приложение для продакшена
RUN npm run build

# Используем легковесный сервер nginx для раздачи статических файлов
FROM nginx:alpine

# Копируем файлы сборки из предыдущего этапа в Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Запускаем сервер Nginx
CMD ["nginx", "-g", "daemon off;"]
