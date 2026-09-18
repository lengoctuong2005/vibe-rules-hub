---
name: quarkus
description: |
  Comprehensive Quarkus 3.x LTS cloud-native suite covering RESTEasy Reactive APIs, CDI & Panache ORM, Event-Driven Camel Messaging, SmallRye JWT & OIDC Security, Test-Driven Development (QuarkusTest, REST-Assured), GraalVM Native Image Compilation, and Verification/Pre-Deployment Gates.
triggers:
  - "quarkus"
  - "panache"
  - "resteasy reactive"
  - "quarkus security"
  - "quarkus tdd"
  - "graalvm native"
  - "smallrye jwt"
license: MIT
metadata:
  origin: ECC
---

# Quarkus Cloud-Native Development Suite

Production-grade engineering guide for high-throughput, low-latency Java applications with Quarkus 3.x LTS and GraalVM Native compilation.

---

## 1. Architecture & Reactive REST APIs

### RESTEasy Reactive Resource & Panache ORM
```java
@Path("/api/v1/orders")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@ApplicationScoped
public class OrderResource {

    @Inject
    OrderRepository orderRepository;

    @GET
    @RolesAllowed("user")
    public Uni<List<Order>> listOrders(@QueryParam("status") OrderStatus status) {
        if (status == null) {
            return orderRepository.listAll();
        }
        return orderRepository.find("status", status).list();
    }

    @POST
    @Transactional
    @RolesAllowed("user")
    public Uni<Response> createOrder(@Valid CreateOrderRequest req, @Context SecurityContext ctx) {
        Order order = new Order(ctx.getUserPrincipal().getName(), req.amount());
        return orderRepository.persist(order)
            .map(saved -> Response.status(Response.Status.CREATED).entity(saved).build());
    }
}
```

### Hibernate with Panache Repository
```java
@ApplicationScoped
public class OrderRepository implements PanacheRepositoryBase<Order, UUID> {
    
    public Uni<List<Order>> findByCustomerEmail(String email) {
        return find("customerEmail", email).list();
    }

    public Uni<Long> updateStatus(UUID orderId, OrderStatus status) {
        return update("status = ?1 where id = ?2", status, orderId);
    }
}
```

---

## 2. Event-Driven Messaging with Apache Camel

```java
@ApplicationScoped
public class OrderEventRoute extends RouteBuilder {

    @Override
    public void configure() {
        from("rabbitmq:amq.direct?queue=orders.incoming&routingKey=order.created")
            .routeId("process-incoming-orders")
            .unmarshal().json(JsonLibrary.Jackson, OrderEvent.class)
            .log(LoggingLevel.INFO, "Processing order event: ${body.orderId}")
            .bean(OrderProcessingService.class, "handleOrderCreation")
            .to("rabbitmq:amq.direct?queue=orders.processed");
    }
}
```

---

## 3. Quarkus Security (SmallRye JWT / OIDC)

### Security Configuration (`application.yaml`)
```yaml
quarkus:
  http:
    auth:
      permission:
        authenticated:
          paths: ["/api/*"]
          policy: authenticated
        admin:
          paths: ["/api/v1/admin/*"]
          policy: roles
          roles: ["admin"]
  smallrye-jwt:
    enabled: true
  security:
    users:
      embedded:
        enabled: false
```

### Programmatic Security Verification
```java
@ApplicationScoped
public class AccountService {

    @Inject
    SecurityIdentity securityIdentity;

    @Inject
    JsonWebToken jwt;

    public void processSensitiveOperation() {
        if (!securityIdentity.hasRole("admin")) {
            throw new ForbiddenException("Administrative privileges required.");
        }
        String tenantId = jwt.getClaim("tenant_id");
        // Execute operation with tenant context
    }
}
```

---

## 4. Test-Driven Development (`@QuarkusTest`)

### REST-Assured Integration Testing
```java
@QuarkusTest
@TestHTTPEndpoint(OrderResource.class)
class OrderResourceTest {

    @Test
    @TestSecurity(user = "testuser", roles = {"user"})
    void shouldCreateOrderSuccessfully() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {
                    "amount": 129.99,
                    "items": ["ITEM-1", "ITEM-2"]
                }
            """)
        .when()
            .post()
        .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("status", equalTo("PENDING"));
    }

    @Test
    void shouldRejectUnauthenticatedRequests() {
        given()
            .contentType(ContentType.JSON)
            .body("{}")
        .when()
            .post()
        .then()
            .statusCode(401);
    }
}
```

---

## 5. GraalVM Native Compilation & Verification Pipeline

Execute before release:

```bash
# 1. Standard JVM Build & Test Suite
mvn clean verify

# 2. GraalVM Native Binary Compilation
mvn package -Dnative -Dquarkus.native.container-build=true

# 3. Native Integration Testing
mvn test-compile failsafe:integration-test -Dnative

# 4. Container Build & Minimal Image Test
docker build -f src/main/docker/Dockerfile.native -t quarkus-service:latest .
```
