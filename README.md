Virtual environemnt setup
close the project and cd into the project directory
cd Orders

Now you are ready to start the docker container:
RUN
docker-compose up

Open your browser and enter the url - http://localhost:8000

Now to run the test cases:
Run the below commands to activate the virtual env or Flask framework

---

macOS:

$ python3 -m venv venv
$ . venv/bin/activate

Windows:

> py -3 -m venv venv
> venv\Scripts\activate

---

python test.py
