# Features
This document contains an overview of each of the desired metrics and models to be delivered as part of comet, the code
metrics and analysis tool, including their respective formulae, priorities and other details.

## Overview

### Metrics

#### Cyclomatic Complexity

##### Description
Indicate complexity of a program. Defined as the number of linearly independent paths within a section of code.

##### Formula
CC = E - N + 2C

Where:
* CC = Cyclomatic complexity.
* E = Number of edges in the control flow graph.
* N = Number of nodes in the control flow graph.
* P = Number of connected components.

##### Priority

#### Logical Lines of Code

##### Description
The number of statements in a section of code, irrespective of whitespace, comments or code style differences.

##### Formula
LLOC = Number of statement nodes in AST.

##### Priority

#### Lines of Comment

##### Description
The number of lines of comment in a section of code.

##### Formula
LOC = Number of lines of comment.

##### Priority

#### Afferent Coupling

##### Description

##### Formula

##### Priority

#### Efferent Coupling

##### Description

##### Formula

##### Priority

#### Instability

##### Description

##### Formula

##### Priority

#### Abstractness

##### Description

##### Formula

##### Priority

#### Method Cohesion

##### Description

##### Formula

##### Priority

#### Relational Cohesion

##### Description

##### Formula

##### Priority

#### Nesting Depth

##### Description

##### Formula

##### Priority

### Models

#### Abstract Syntax Tree (AST)

##### Description

##### Priority

#### Control Flow Graph (CFG)

##### Description

##### Priority

#### Inheritance Tree

##### Description

##### Priority

#### Class Diagram

##### Description

##### Priority

## Priorities

| Feature               | Priority |
|-----------------------|----------|
| Cyclomatic Complexity |          |
| AST                   |          |
| CFG                   |          |
| Inheritance Tree      |          |
