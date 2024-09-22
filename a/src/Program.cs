using System.Reflection;
using HealthChecks.UI.Client;
using LetterA.Controllers.V1;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.AspNetCore.Mvc.ActionConstraints;
using Microsoft.AspNetCore.Mvc.Infrastructure;
using Microsoft.EntityFrameworkCore;
using NDjango.RestFramework.Extensions;
using NDjango.RestFramework.Serializer;
using Newtonsoft.Json;
using Serilog;

var solutionSettings = Path.Combine(Directory.GetCurrentDirectory(), "..", "appsettings.json");
if (!File.Exists(solutionSettings))
    solutionSettings = Path.Combine(Directory.GetCurrentDirectory(), "appsettings.json");

var configuration = new ConfigurationBuilder()
    .AddJsonFile(solutionSettings, optional: false, reloadOnChange: false)
    .AddEnvironmentVariables()
    .Build();

Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(configuration)
    .CreateLogger();

Log.Information("Logger initialized. Starting up the application.");

configuration["ASPNETCORE_URLS"] = configuration["ASPNETCORE_URLS"] is null ? "http://+:8000" : configuration["ASPNETCORE_URLS"];

try
{
    var builder = WebApplication.CreateBuilder(args);

    builder.Host.UseSerilog();
    builder.Configuration.AddConfiguration(configuration);

    var connectionStringDatabase = configuration.GetConnectionString("AppDbContext");
    var connectionStringBroker = configuration.GetConnectionString("Broker");
    builder.Services.AddDbContext<AppDbContext>(options =>
    {
        options.UseSqlServer(connectionStringDatabase);
    });
    
    // Add services to the container.
    builder.Services.AddControllers()
        .AddNewtonsoftJson(config =>
        {
            config.SerializerSettings.ReferenceLoopHandling = ReferenceLoopHandling.Ignore;
            config.SerializerSettings.NullValueHandling = NullValueHandling.Ignore;
        })
        .ConfigureValidationResponseFormat();
    // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
    // Update it to another library in the future: https://github.com/dotnet/aspnetcore/issues/54599
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen(options =>
    {
        var whereFilesAre = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        foreach (var filePath in Directory.GetFiles(Path.Combine(whereFilesAre!), "*.xml"))
        {
            try
            {
                options.IncludeXmlComments(filePath);
            }
            catch (Exception e)
            {
                Log.Error(e, "Error while trying to include XML comments from {FilePath}", filePath);
            }
        }
    });
    builder.Services.AddHealthChecks()
        .AddSqlServer(connectionStringDatabase!, tags: ["crucial"])
        .AddRabbitMQ(new Uri(connectionStringBroker!));
    // NDjango Rest framework configuration
    builder.Services.AddScoped<Serializer<PersonDto, Person, int, AppDbContext>>();
    builder.Services.AddScoped<Serializer<TodoItemDto, TodoItem, int, AppDbContext>>();
    
    var app = builder.Build();
    app.MapControllers();

    // Configure the HTTP request pipeline.
    app.UseSwagger();
    app.UseSwaggerUI();
    app.MapGet("/debug/routes", (IActionDescriptorCollectionProvider provider) =>
    {
        return provider.ActionDescriptors.Items.Select(actionDescriptor => new
        {
            Action = actionDescriptor.RouteValues["Action"],
            Method = actionDescriptor.ActionConstraints!.OfType<HttpMethodActionConstraint>().FirstOrDefault()?.HttpMethods.FirstOrDefault(),
            Controller = actionDescriptor.RouteValues["Controller"],
            Name = actionDescriptor.AttributeRouteInfo!.Name,
            Template = actionDescriptor.AttributeRouteInfo.Template
        }).ToList();
    });
    app
        .UseHealthChecks("/healthcheck/liveness",
            new HealthCheckOptions
            {
                Predicate = _ => false,
                AllowCachingResponses = false,
                ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
            })
        .UseHealthChecks("/healthcheck/readiness",
            new HealthCheckOptions
            {
                Predicate = targetHealthCheck => targetHealthCheck.Tags.Contains("crucial"),
                AllowCachingResponses = false,
                ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
            })
        .UseHealthChecks("/healthcheck/integrations",
            new HealthCheckOptions
            {
                Predicate = _ => true,
                AllowCachingResponses = false,
                ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
            });
    // Apply migrations
    using var scope = app.Services.CreateScope();
    using var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    if (dbContext.Database.GetPendingMigrations().Any())
        dbContext.Database.Migrate();
    
    await app.RunAsync();
}
catch (Exception ex) when (ex is not HostAbortedException && ex.Source != "Microsoft.EntityFrameworkCore.Design")
{
    // Why did I have to do this? Check this issue: https://github.com/dotnet/efcore/issues/29923#issuecomment-2092619682
    Log.Fatal(ex, "Host terminated unexpectedly");
}
finally
{
    await Log.CloseAndFlushAsync();
}

// Allows tests with WebApplicationFactory
// https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-8.0#basic-tests-with-the-default-webapplicationfactory-1
public partial class Program
{
}
