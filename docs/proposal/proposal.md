# School of Computing &mdash; Year 4 Project Proposal Form

## SECTION A
|Project Title:       | comet - Code Metrics and Analysis Tool|
|---------------------|---------------------------------------:|
|Student 1 Name:      |                         Kevin McGonigle|
|Student 1 ID:        |                                16318486|
|Student 2 Name:      |                             James Miles|
|Student 2 ID:        |                                16349533|
|Project Supervisor:  |                      Dr. Geoff Hamilton|

## SECTION B

### Introduction
For our final year project, we propose the development of an easy-to-use but powerful and comprehensive code metrics and analysis tool. This end-goal is for this tool to take the form of an IDE plugin to display useful data relating to the performance, structure and style of a codebase in a clear and intuitive manner.

### Outline
The tool that we plan to develop will provide the end user with a deeper understanding of their codebase, through the use of metrics such as cyclomatic complexity and maintainability index, and by creating useful and easy to understand graphs and diagrams relating to class relationships, test coverage and other analytics that can be scaled to the desired level of detail for a more general or specific overview. All of this will be computed on a back-end server and displayed to the user in a responsive, consistent and attractive user interface that allows for viewing multiple or specific metrics and is simple to navigate.

### Background
The basis for idea was formed as a consequence of both of us having worked with large codebases as part of our INTRA placements, the likes of which often prove to be daunting and confusing, especially to those who are unfamiliar with it. We both struggled at times to get to grips with such a broad and complicated codebase, often finding ourselves going down the wrong path to get to where we need to be, or suffering because of overly complex and under documented segments of code. We also experienced a lack of cohesiveness and consistency between requirements, design, implementation and testing that served only to add to the confusion.

This confusion prompted the same response in both of us, and we both came up with different but closely related ideas for tools to rectify the problem. One of these ideas was for a code metrics tool, for displaying various measurements relating to the performance of code. The other involved a tool for seamlessly converting standardised diagrams such as class diagrams into blank, object-oriented code, as well as deriving such diagrams from a codebase. After some detailed discussion, we arrived at a solution to incorporate the best concepts from both ideas to deliver a complete, comprehensive tool for users of all levels to understand and improve their code in a variety of ways.

### Achievements
Our project will be designed and created with every level of developer in mind and we will endeavour to ensure that our finished product is both sufficiently usable and educational for the novice programmer as well as robust and feature-rich enough to satisfy the more advanced user.

In terms of functionality, we will seek to compute and display the following metrics, analytics and resources in a concise and intelligent manner.
- Cyclomatic Complexity
- Maintainability Index
- Class Diagram
- Technical Debt
- Test Coverage
- Comment Coverage
- Coupling
- Abstractness
- Inheritance Tree
- Nesting Depth
- Class/Method Summaries

### Justification
We believe that such a tool would be useful for a number of reasons. The most prominent reason would be that it would allow the developer to enhance their understanding of their code, how it works, and how it could be improved on both performance and structural bases. This would allow developers to produce more maintainable, robust and concise code that is readable and easily understood. The tool would help developers that work with complex and convoluted codebases and are looking to refactor them or simply to understand its functionality.

Our project also lends itself as an educational resource, affording novice users with clear explanations of what certain metrics mean and how they affect program performance and maintainability, as well as helping them to understand the code that they're writing with comprehensible diagrams and graphs. Ultimately, we believe that our project would be a practical resource that should improve the development experience across the board.

### Programming Language(s)
We plan to use Python to handle all back-end operations, using Django alongside Swagger to create an API-based infrastructure that will parse, execute and return the results for any requests made by the front-end. This front-end user interface will be created Javascript (with React and Redux), HTML and CSS, and will be used to allow input from the user and to display the returned data. 

### Programming Tools / Tech Stack
#### Swagger
A framework backed by a large ecosystem of tools that helps developers design, build, debug, document, and consume RESTful web services. Swagger aids in development across the entire API lifecycle, and will hopefully greatly improve our design, development, documentation & deployment processes.

#### React/Redux
A JavaScript library for building modular user interfaces. This will enable us to build encapsulated, testable and simple components which may then be utilised for the composition of larger, more complex components. Redux allows these React components to fetch data from the Redux Store and dispatch actions to update the store.

#### Node
A JavaScript run-time environment that executes JavaScript code outside of a browser. Node.js lets developers use JavaScript to write command line tools and for server-side scripting, i.e. running scripts server-side to produce dynamic web page content before the page is sent to the user's web browser.

### Hardware
We will have no unusual hardware requirements for the creation or usage of our project. We will however be making use of an Amazon Web Services EC2 instance to serve as a host for the back-end of our solution.

### Learning Challenges
In order for a user to have the best experience possible, we need to ensure efficiency within the metric calculation algorithms. Inefficient algorithms will create longer wait times between API calls, which could frustrate the user. We will therefore need to research this carefully and challenge ourselves to deliver efficient code.

Alongside this we will need to create a generic language parser that can be fed a list of rules and text, which will then produce some form of AST from the parsed data, something that neither of us have had to do before and will certainly pose a difficult but rewarding and insightful challenge. 

Although relatively (and in some cases exceptionally) comfortable with all of the languages that we have chosen to use, we both have somewhat limited experience working with React, Redux and JavaScript as a whole which means we will be required to develop our understanding and familiarity with the tools provided by the languages to employ them to their fullest potentials.

### Breakdown of Work
In general, we have decided to divide the work for all aspects of our project as evenly as possible. We will both be playing an active role in the design, development and testing of both the front and back ends of the application, dividing the work based on functionality from start to finish rather than restricting one an other to either server-side or user-facing development. In doing so, we will both gain vital experience working with all facets of our project so that we each have a comprehensive understanding of the architecture and functionality of the system.

To manage our work process, we plan to use an issue-tracking service to enforce accountability and ensure that development is progressing on time and is producing high-quality output. We had hoped to use Jira Software for this, each of us having worked closely with it while on our placements; however, we have decided to opt for a Trello board to avoid the costs that Jira incurs.

#### Kevin McGonigle
In keeping with what was stated above, I will be participating heavily in every deliverable for the upcoming project, from the design phase right the way through to testing and documentation.

Without having planned out on a low-level basis the specific tasks that each of us will be undertaking, something that we plan to do in an agile fashion as the project progresses, I have agreed to take the lead on the design, development and verification of the following metrics and analytics:
- Cyclomatic Complexity
- Technical Debt
- Test Coverage
- Comment Coverage
- Nesting Depth

I will also be taking the lead in setting up the "back-end server" on an Amazon EC2 instance, having gained experience working with such technology on my third year project.

#### James Miles
- Maintainability Index
- Class Diagram
- Class/Method Summaries
- Coupling
- Abstractness
- Inheritance Tree