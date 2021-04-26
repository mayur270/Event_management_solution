### Thought Process

1. The first step in this process was to design the layout of the application and what fields are 
important in addition to the stated ones in the test. Online tools like figma can help in designing.

2. The next stage started with the backend in building models (Event and Ticket) and connecting the 
relationship between them with ForeignKey. This was used since one event would have multiple tickets.
 
3. The next phrase was building serializer and views. The serializer.py transform data into json 
format for the frontend to receive. The views are written in ViewSet. I have not included routers in 
this test since it is a small application. Once the views are written, urls need to be added in urls.py file.

4. Unit tests are then to be added to help with any errors. Library such as django-nose was installed.

5. Frontend Development can then be build for this specific view(s) and data can be fetched using axios.
