# Unit 3 Project: CK Feedback Software

![DALLE](/assets/documentation/DALL·E.png)
<i> A pixel art of a person cooking some pancakes in a 3d cubic kitchen </i>

# Criteria A: Planning

## Problem definition

Cezar KItchen is a high school cafeteria that serve students and staff in UWC ISAK Japan. The cafeteria is managed by a Dariosan and has a student representative named Thumula Ayodhya Karunaratne. Until recently there was a notebook near the exit where you could write feedback about the lunch that you just eat, but because people where using it just to spam two things (karage and apple crumble), therefore the notebook was removed. One day Thumula had the idea to create a device that could take feedback at the exit like the ones after the security check in airports. Because the number of dishes could change it was opted for a numerical feedback system. Also to have a more specific feedback, the device should have a screen where the user could write a comment. The device should also have a login system for the management to see the feedback and the comments. 

## Succes Criteria

1. Working Fast Feedback System
2. Working Additional Feedback System (add/edit/delete)
3. Enjoyable User Experience (The program will be built using a Material Design framework and employ a unfied color theme)

## Design Statement 

Looking at the clients requirements the best solution for this feedback system would be a tablet with a set of buttons to allow the user to add a quick one-click feedback and a second button to allows to a more dish specific feedback. Because Dariosan usually dosen't uses his computer oftenly it would be better to make the feedback availeble for review dirrectly on the feedback screen.

For the back end management we decided to use python because it is a language that I am familiar with and it is easy to use, and because this is a small project performance is not a big issue.
For the GUI design we decided that using kivy would be the best option because I already had some experience with it and it would be easy to implement with the database because it a framework that uses python. Even if flutter would be a better option at every aspect [^2], it would be too much work to learn it in such a short time for this kind of short project. I used the add-on library KivyMD to make it easier to implement and edit.

## Rationale for Proposed Solution

Todo



# Criteria B: Design

## System Diagram

![System Diagram](assets/documentation/System.png)

## Wireframe

![wireframe](assets/documentation/Wireframe.png)

## Er Diagram

![ER](assets/documentation/ER.png)

## UML Diagram

![UML](assets/documentation/UML.png)

## Flow Diagram

## Test Plan

## Record of task

| Task No | Planned Action                                   | Planned Outcome                                          | Time estimate | Target completion date | Criterion |
| ------- | ------------------------------------------------ | -------------------------------------------------------- | ------------- | ---------------------- | --------- |
| 1       | Planning: First Meeting with client              | Start collecting the context of the problem              | 6 min         | Feb 7                  | A         |
| 2       | Planning: Defining problem and proposed solution | Start on refining client's requirements and tools needed | 60 min        | Feb 20                 | A         |

## 

# Criteria C: Development

## Techniques used

1) Objected Oriented Programming (OOP)
2) ...

## Development of User Interface Using KivyMD

### Screen Manager

\```.kv



\```



# Criteria D: Functionality







# Appendix

## Evidence of consultation

# Criteria B: Design

## System Diagram

*Later

**Fig.1** 

## Data Storage



## Wireframe



## Record of Tasks

| Task No | Planned Action                                   | Planned Outcome                                          | Time estimate | Target completion date | Criterion |
| ------- | ------------------------------------------------ | -------------------------------------------------------- | ------------- | ---------------------- | --------- |
| 1       | Planning: First Meeting with client              | Start collecting the context of the problem              | 6 min         | Feb 7                  | A         |
| 2       | Planning: Defining problem and proposed solution | Start on refining client's requirements and tools needed | 60 min        | Feb 20                 | A         |

## Flow Diagrams

### MVP Program

![](Assets/MVP_FD2.jpg)

*Fig.2* **Flow diagram for the MVP program.**

### Main Program

![](Assets/MAIN_FD2.jpg)

*Fig.3 **Flow diagram for the main program.**

## Test Plan

| Type    | Input | Process | Anticipated Outcome |
| ------- | ----- | ------- | ------------------- |
| *Insert |       |         |                     |
|         |       |         |                     |

# Criteria C: Development



## Existing Tools ?

| Software/Development Tools | Coding Structure Tools | Libraries |
| -------------------------- | ---------------------- | --------- |
| *Insert                    |                        |           |

## List of techniques used

1. 

## Computational Thinking

### Decomposition

In computational thinking, decomposition refers to breaking a complex problem or system into parts that are easier to conceive,
understand, program, and maintain.

### Pattern recognition, generalization and abstraction



### Algorithms

## Development of User Interface Using KivyMD

### Screen manager
BlaBlaBla


## Development

### OOP

### ORM

### Other nice techniques to use


# Criteria D: Functionality
## Video Showcasing the Functionality of the Application
Video link: 

## Evidence of Testing

### Database Integrity Testing
This pytest is a fast test you can run before the running of the program to make a quick check of the integrity of the database. It is not a complete test but it is a good start to make sure that the database is working properly.
```.py
import pytest

from database_handler import DatabaseHandler


def test_create_db():
    # Test that create_db() function returns None
    assert create_db() is None


def test_add_dish():
    # Create a DatabaseHandler instance
    db_handler = DatabaseHandler()

    # Add a dish and check if it returns None
    assert db_handler.add_dish('Spaghetti', 'Italian', 'Pasta, Tomato sauce, Meat') is None

    # Query the dishes with input search string 'hett'
    dishes = db_handler.query_dishes('hett')
    
    # Assert that the recently added dish 'Spaghetti' is in the result list 
    assert any(dish.name == 'Spaghetti' for dish in dishes)

    # Close the session
    db_handler.close()
```
*Fast Main Test (if you was to test the main things)*

### All Database Handler Functions Testing
This pytest is a more complete test that tests all the functions of the database handler. It is a bit slower than the previous one but it is useful to check if the modifications you did to the handler are working properly.

Importing the Handler and the libraries
```.py
from datetime import date, datetime
from database_handler import DatabaseHandler
import pytest
```

Nice trick that i forgot to implement (avoiding to leave the database open)
```.py
@pytest.fixture(scope="function")
def session():
    db = DatabaseHandler()
    yield db.session
    db.close()
```

Testing all the functions
```.py

```








# Appendix

## Evidence of Consultation

### Client approval of proposed success critereas


### Client's review of application during development process


### Client's review of final product


# Citations

RSS, https://www.adafruit.com/product/386.
[^2]: Educba. "Kivy vs Flutter" Educba, https://www.educba.com/kivy-vs-flutter/