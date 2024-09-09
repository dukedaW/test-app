FROM python:3.12
LABEL authors="macbook"
WORKDIR /test-app
COPY ./instance /test-app/instance
COPY ./templates /test-app/templates
COPY app.py buyer.py index.py main.py product.py purchase.py report.py requirements.txt /test-app/
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["main.py" ]