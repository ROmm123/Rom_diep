
FROM python:3.11

WORKDIR /app


COPY SERVER4.py /app/

EXPOSE 44440/tcp
EXPOSE 44445/tcp

CMD ["python", "SERVER4.py"]
