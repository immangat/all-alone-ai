### State Space Generator Requirements Checklist

1. **Input Handling**
   - [ ] Read input from Test<#>.input files.
   - [ ] Parse input to determine the color of marbles and their positions.

2. **Legal Moves Generation**
   - [ ] Generate all possible legal next-ply moves (in-line and side-step).
   - [ ] Consider the color of the marbles and the game board boundaries.

3. **Resulting Game Board Configurations**
   - [ ] Generate all resulting game board configurations for each legal move.
   - [ ] Ensure no duplicate game board configurations are generated.

4. **Output Generation**
   - [ ] Write the list of legal moves to Test<#>.move files.
   - [ ] Write the corresponding resulting game board configurations to Test<#>.board files.

5. **File Formats**
   - [ ] Follow the specified file formats for Test<#>.input, Test<#>.move, and Test<#>.board.

6. **Testing and Verification**
   - [ ] Test the state space generator with provided sample input/output files.
   - [ ] Create additional test cases to verify the correctness of the implementation.

7. **Documentation**
   - [ ] Indent and comment code based on best practices.
   - [ ] Include a State Space Generator report (part2report_groupnumber.pdf) with the following:
     - State Representation, Actions, and Transition Model used
     - Design and architecture of the State Space Generator
     - Move Notation (team-defined) used in Test<#>.move
     - Team member contributions
     - List of references used
     - Any additional documentation pertinent to the assessment

8. **Submission**
   - [ ] Submit the State Space Generator report (part2report_groupnumber.pdf) by Mar 21, 2024.
   - [ ] Submit the source code and executable (part2sourcecode_groupnumber.zip) by Mar 21, 2024.

9. **Compliance**
   - [ ] Ensure compliance with BCIT Policy 5104 (standards of conduct).

10. **Final Deliverables**
    - [ ] No late submissions will be accepted.
    - [ ] Only one submission is allowed.

### Upcoming Due Dates
- Mar 28, 2024: Project Part #3 - Search Strategy and Optimization.
- Apr 4, 2024, Apr 11, 2024: Project Part #4 - Tournament and Final Deliverable.
