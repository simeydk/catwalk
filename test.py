from actuary import project, Policy


print(project(Policy(age=20, premium=100, sum_assured=100000, term=1080), proj_term_m=1200))
# print(project(Policy(age=30, premium=100, sum_assured=100000, term=999), proj_term_m=1200))
# print(project(Policy(age=30, premium=100, sum_assured=100000, term=999), proj_term_m=1200))