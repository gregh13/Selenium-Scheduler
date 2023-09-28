FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

# Bash style commange
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD goes at end, it starts the program. Can only be one CMD
CMD [ "python", "./main_scheduler.py" ]



