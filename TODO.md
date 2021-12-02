Done
    num_of_days = models.FloatField(verbose_name='number of days')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

-Let's add verbose_name with '{name} (Auto-calculated)'
class Query(graphene.ObjectType):
    leaves = graphene.List(LeaveType)
    leave_by_id = graphene.Field(LeaveType, id=graphene.String())
    leave_day = graphene.List(LeaveDayType)
- remove leave_day and edit leave_by_id to leave
def __str__(self):
    return self.first_name + " " + self.last_name
    return " %s %s " % (self.first_name, self.last_name)
- use get_full name
- Remove RemoveNullFieldsMixin, DynamicFieldsMixin


- Function to calculate number of days
- Make number of days , start date , end date readonly.
- add leave status to be Approved by default
- Add type = NO_LEAVE in LeaveDay
- validation.
    - start_date has to smaller or equal to end date
    - cannot apply paid leave after exceeding max paid leave days
    - No dublicate leave
- return multiple days or single day in leave query
- remove week days from leave apply


- modified validation for existing leave
- Provide api to query leavetypes, leave day types

To Do:

- test case  for apply leave
- update leave
- add created_for in leave model
- Need to adjust total sum incase of other not countable leaves
- Remove password from user fixtures


