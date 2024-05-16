
FROM python:3.11

WORKDIR /app
COPY main_server.py HP.py connection_with_database.py random_pos_npc.py Random_PosObj.py /app/

RUN pip install pygame mysql-connector-python

EXPOSE 55555/TCP
EXPOSE 55556/TCP
EXPOSE 55557/TCP
EXPOSE 64444/TCP
EXPOSE 55558/TCP

CMD ["python", "main_server.py"]