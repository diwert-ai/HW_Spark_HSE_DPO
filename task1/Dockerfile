
# Используем в качестве базового образа образ python
FROM python:3.11-slim

# Создайте папку, в которой будет храниться исходные файлы приложения, с именем app
# YOUR CODE HERE
RUN mkdir /app 

# Пометьте созданную папку app как рабочую директорию. 
# YOUR CODE HERE
WORKDIR /app

# Перекопируйте файл server.py с текущей директории в созданную выше папку app
# YOUR CODE HERE
COPY server.py /app
# Перекопируйте файл словаря c текущей директории в созданную выше папку app
# YOUR CODE HERE
COPY dictionary.txt /app

# Установим библиотеку Flask внутрь контейнера
RUN pip3 install -q Flask

# Сделаем порт 5555, на котором работет приложение видимым
EXPOSE 5555

# Установим команду, которая будет запускаться при старте котнейнера
CMD ["python3", "server.py"]
