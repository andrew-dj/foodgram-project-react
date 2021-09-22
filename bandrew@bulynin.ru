version: '3.3'
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    volumes:
      - ./frontend/:/app/result_build/
  db:
    image: postgres:13.3
    ports:
      - 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data/

    env_file:
      - ./backend/.env
  backend:
    image: bandrew8544/foodgram-project-react
    restart: always
    volumes:
      - static_value:/code/static/
      - media_value:/code/media/
    depends_on:
      - db
    env_file:
      - ./backend/.env
  nginx:
    image: nginx:1.19.3
    restart: always
    ports:
      - 80:80
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./frontend/build:/usr/share/nginx/html/
      - static_value:/var/html/static/
      - media_value:/var/html/media/
    depends_on:
      - backend
volumes:
  postgres_data:
  static_value:
  media_value:
