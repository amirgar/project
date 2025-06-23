# Подключаем пакет языка Go
FROM golang:1-alpine AS build

# Задаем необходимые переменные
ENV CGO_ENABLED=0
ENV GOOS=linux

# Рабочая директория, задает рабочий каталог
WORKDIR /go/src/github.com/united-manufacturing-hub/benthos-umh

# Запуск кода в контейнере с командой Run
RUN apk update --no-cache && apk upgrade && \
  apk add --no-cache ca-certificates git wget && \
  update-ca-certificates &>/dev/null && \
  git clone https://github.com/united-manufacturing-hub/benthos-umh.git -b v0.5.2 /go/src/github.com/united-manufacturing-hub/benthos-umh && \
  go mod download && \
  go build -o ./main cmd/benthos/main.go

# Указываем еще один родительский образ, причем теперь это многоступенчатый образ, на предыдущие этапы не смотрит для экономии памя 
FROM busybox

# Копируем все файлы и вставляем в наш контейнер
COPY --from=build /go/src/github.com/united-manufacturing-hub/benthos-umh/main connect

# Через данный порт можно будет связаться с контейнером
EXPOSE 4195

# Задаём функцию, которая будет обязательно выполняться при запуcке контейнера
ENTRYPOINT ["/connect"] 
