using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public DbSet<Person> Persons { get; set; }
    public DbSet<TodoItem> TodoItems { get; set; }

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
        // Bodyless constructor
    }

    public static AppDbContext CreateContext(string connectionString,
        DbContextOptionsBuilder<AppDbContext>? optionsBuilder = null)
    {
        if (optionsBuilder is null)
            optionsBuilder = new DbContextOptionsBuilder<AppDbContext>();

        optionsBuilder.UseSqlServer(connectionString);
        var options = optionsBuilder.Options;

        return new AppDbContext(options);
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // More details about the EF Fluent API in the following links:
        // https://docs.microsoft.com/en-us/ef/ef6/modeling/code-first/fluent/relationships#configuring-a-many-to-many-relationship
        // https://docs.microsoft.com/en-us/ef/ef6/modeling/code-first/fluent/types-and-properties
        modelBuilder.Entity<Person>(entity =>
        {
            entity.Property(p => p.Name).IsRequired().HasMaxLength(100);
            entity.HasIndex(p => p.Name).IsUnique();
        });
        modelBuilder.Entity<TodoItem>()
            .HasOne(todoItem => todoItem.Person)
            .WithMany(user => user.TodoItems)
            .HasForeignKey(todoItem => todoItem.UserId);
    }

    public override int SaveChanges()
    {
        AutomaticallyAddCreatedAndUpdatedAt();
        return base.SaveChanges();
    }

    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        AutomaticallyAddCreatedAndUpdatedAt();
        return base.SaveChangesAsync(cancellationToken);
    }

    private void AutomaticallyAddCreatedAndUpdatedAt()
    {
        var entitiesOnDbContext = ChangeTracker.Entries<StandardEntity>();

        if (entitiesOnDbContext is null)
            return;

        foreach (var item in entitiesOnDbContext.Where(t => t.State == EntityState.Added))
        {
            item.Entity.CreatedAt = DateTime.Now.ToUniversalTime();
            item.Entity.UpdatedAt = DateTime.Now.ToUniversalTime();
        }

        foreach (var item in entitiesOnDbContext.Where(t => t.State == EntityState.Modified))
        {
            item.Entity.UpdatedAt = DateTime.Now.ToUniversalTime();
        }
    }
}
