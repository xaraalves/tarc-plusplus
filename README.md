# tarc-plusplus
A Quick Example Applying IoT Sensors and Twython to Simulate a Smart City Scenario

This project aims to simulate a very restrict scenario that would occur in most of smart cities: the detection of possible flood or earthquake.

To do so, we analyze messages posted on Twitter and the results that are given from the sensors attached to the board. If an event is detected, we send notifications via Twitter and Facebook to the users nearby.

We have a centralized system, as shown in the image above. Its core runs on a Debian/Ubuntu computer, receiving the collected data from the sensors (on the DragonBoard) and sending them to AWS IoT via MQTT protocol. The computer then gets these data from AWS IoT (subscribing to the corresponding topics), processes it (within the result of the search by keywords on Twitter) and fires the necessary notifications (to Facebook and Twitter).
