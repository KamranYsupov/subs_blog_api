FROM python:3.11

WORKDIR /subs_blog

COPY . .

COPY requirements.txt /temp/requirements.txt

EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install /temp/requirements.txt

CMD ["python", "manage.py", "runserver"]