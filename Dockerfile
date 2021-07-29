FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN cp netrc_sample ~/.netrc
RUN apt install -y curl \ 
    apt install -y nodejs
RUN npm install -g heroku
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["bot.py"]
ENTRYPOINT ["python3"]
