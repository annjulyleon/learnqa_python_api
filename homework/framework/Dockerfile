FROM python
WORKDIR /tests_projects/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV ENV=dev
ENV TZ=Europe/Moscow
CMD python -m pytest -s --alluredir=test_results/ /tests_projects/tests/