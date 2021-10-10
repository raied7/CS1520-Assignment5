# CS1520-Assignment5

**Due Oct 17 by 11:59pm Points 25 Submitting a file upload Available Oct 9 at 12am - Oct 17 at 11:59pm**

Now that we've built some classes for chat messages, we can deploy them to Google App Engine. You can deploy this example to see a working chat application: 

https://drive.google.com/file/d/1YItPFthsL1nnSQOn1x8QdtlixoQI5sC1/view?usp=sharing (Links to an external site.)

Unfortunately, the messages are not stored. If our machine crashes, or if another server starts up, or if our requests are sent to different locations, our experience will be significantly diminished. 

Your goal is to extend this example so that messages are stored using Cloud Datastore. You'll want to modify message.py and enhance the ChatManager class so that add_message, create_message, get_messages_output, get_messages_html, and clear_messages_before work with the Cloud Datastore. You'll want to persist (and delete) messages as appropriate and not rely on the server's memory.

You may want to look at https://github.com/timothyrjames/gae-webdev/tree/main/step09 (Links to an external site.) for examples of how to store, retrieve, and delete data.

Please submit your completed message.py file here (as well as any other files that you modify or add for this assignment).
