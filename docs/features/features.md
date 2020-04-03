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
* E = Number of edges in the control flow graph.
* N = Number of nodes in the control flow graph.
* C = Number of connected components.

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
The number of other packages/types/methods that depend on a given package/type/method. This indicates how dependent
other packages/types/methods are on the examined artifact. An AC value of zero indicates potentially "dead" code that is
not in use.

##### Formula
AC = Number of arrows pointing to dependency graph node.

##### Priority

#### Efferent Coupling
The number of other packages/types/methods that are depended upon by a given package/type/method. This indicates how
dependent the examined artifact is on other packages/types/methods.

##### Description
EC = Number of arrows pointing away from dependency graph node.

##### Formula

##### Priority

#### Instability

##### Description
The ratio of efferent coupling to total coupling, indicating a package/type/method's resilience to change.

##### Formula
I = EC / (EC + AC)

Where:
* EC = Efferent coupling.
* AC = Afferent coupling.

##### Priority

#### Abstractness

##### Description
The ratio of the number of abstract types/methods to the number of total types/methods (both abstract and concrete).

##### Formula
A = AB / (AB + CO)

Where:
* AB = Number of abstract types/methods.
* CO = Number of concrete types/methods.

##### Priority

#### Method Cohesion

##### Description
A measurement of a class's adherence to the single responsibility principle by examining how many instance fields are 
used in each method.

##### Formula
MC = MF / (M * F)

Where:
* MF = The sum of the number of methods using a given instance field for each instance field of the class.
* M = The number of methods in the class.
* F = The number of instance fields in the class.

##### Priority

#### Relational Cohesion

##### Description
The number of internal relationships per type, giving an indication of coupling within a package.

##### Formula
RC = R / T

Where:
* R = The number of internal relationships.
* T = The number of types.

##### Priority

#### Nesting Depth

##### Description
The maximum number of encapsulated scopes within a given method, indicating complexity and maintainability.

##### Formula
ND = Maximum number of encapsulated scopes.

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

#### Dependency Graphs

##### Description

##### Priority
