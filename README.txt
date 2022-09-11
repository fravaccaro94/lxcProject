This python program aims to automate the creation of a platform for a distributed web application. 

The application is composed of several components: a Node.js application with mongoose (MVC), a database MongoDB, a load balancer and a client.

The Node.js application is deployed in multiple servers (linux containers) connected to a load balancer that reparts the traffic along the server with a round robin algorithm.

The application is also connected to a databases in order to have consistency.

The load balancer is a HAPROXY.

The main script is called pfinal.py and it runs the automated process of develop the all platform. When you execute the command python3 pfinal2.py you need to insert a third string choosing between: crear, arrancar, parar and borrar.

When choosing create you also need to pass a second parameter which is the number of the server you want to deploy. It has to be in the between 1 and 5. This function will create the whole platform, its components and set the networking parameters. 

Note that the application is already built in the images from where the containers are created. 

When the platform is created you need to configure the platform in order to establish connection with the command "python3 pfinal2.py configurar".

The previous command creates a proxy to establish connection between the physical machine, where the browser is running, and the containers.

When the platform is configured you need to writ in the command line "python3 pfinal2.py arrancar". This will start all the servers, the load balancer, and the database. It also starts the node application on the servers. 

The command "python3 pfinal2.py parar" stops all the containers and services. To restart the service just type the arrancar command

Finally, "python3 pfinal2.py borrar" deletes all the components and the network.

