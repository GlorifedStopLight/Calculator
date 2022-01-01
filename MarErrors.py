

class InvalidExponentUsage:
    # user inputs something like 7^1 instead of 7^{1}
    # this is raised when specifically ^ exists but not ^{
    # checked after removing spaces
    pass