using Microsoft.AspNetCore.Mvc;
using NDjango.RestFramework.Base;
using NDjango.RestFramework.Filters;
using NDjango.RestFramework.Serializer;

namespace LetterA.Controllers.V1;

public class PersonDto : BaseDto<int>
{
    public string Name { get; set; }
}

[ApiController]
[Route("api/v1/[controller]")]
public class PersonsController : BaseController<PersonDto, Person, int, AppDbContext>
{
    public PersonsController(
        Serializer<PersonDto, Person, int, AppDbContext> serializer, 
        AppDbContext context,
        ILogger<Person> logger
        ) : base(serializer, context, logger)
    {
        AllowedFields =
        [
            nameof(Person.Name)
        ];
        
        Filters.Add(new QueryStringFilter<Person>(AllowedFields));
        Filters.Add(new QueryStringIdRangeFilter<Person, int>());
    }
}
