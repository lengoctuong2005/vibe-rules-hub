---
name: springboot
description: |
  Comprehensive enterprise Spring Boot suite covering Layered Architecture (Controllers, Services, Repositories, DTOs), Spring Data JPA & Transactions, Spring Security (JWT, OAuth2, RBAC, @PreAuthorize), Test-Driven Development (JUnit 5, Mockito, MockMvc, Testcontainers), and Verification/Pre-Deployment Gates.
triggers:
  - "springboot"
  - "spring boot"
  - "spring security"
  - "spring data jpa"
  - "spring tdd"
  - "java backend"
  - "testcontainers"
license: MIT
metadata:
  origin: ECC
---

# Spring Boot Enterprise Development Suite

Production-grade engineering guide for building, testing, securing, and operating enterprise Java applications with Spring Boot 3.x.

---

## 1. Architecture & Layered API Design

### Controller → Service → Repository Flow
```java
@RestController
@RequestMapping("/api/v1/orders")
@Validated
public class OrderController {
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(
        @Valid @RequestBody CreateOrderRequest request,
        @AuthenticationPrincipal UserPrincipal principal
    ) {
        OrderResponse response = orderService.createOrder(principal.getId(), request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<Page<OrderResponse>> listOrders(
        @PageableDefault(size = 20, sort = "createdAt", direction = Sort.Direction.DESC) Pageable pageable,
        @AuthenticationPrincipal UserPrincipal principal
    ) {
        return ResponseEntity.ok(orderService.getUserOrders(principal.getId(), pageable));
    }
}
```

### Global Exception Handling (`@RestControllerAdvice`)
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ProblemDetail handleNotFound(EntityNotFoundException ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(err -> 
            errors.put(err.getField(), err.getDefaultMessage()));
        problem.setProperty("errors", errors);
        return problem;
    }
}
```

---

## 2. Spring Data JPA & Transactions

### Repository with Custom Queries & Projections
```java
@Repository
public interface OrderRepository extends JpaRepository<Order, UUID> {
    
    // Derived query with pagination
    Page<Order> findByUserId(UUID userId, Pageable pageable);

    // Explicit JPQL with fetch join to prevent N+1 queries
    @Query("SELECT o FROM Order o JOIN FETCH o.items i JOIN FETCH i.product WHERE o.id = :id")
    Optional<Order> findByIdWithDetails(@Param("id") UUID id);
}
```

### Transaction Management
```java
@Service
public class OrderService {
    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @Transactional(readOnly = true)
    public Page<OrderResponse> getUserOrders(UUID userId, Pageable pageable) {
        return orderRepository.findByUserId(userId, pageable).map(OrderResponse::from);
    }

    @Transactional
    public OrderResponse createOrder(UUID userId, CreateOrderRequest req) {
        Order order = new Order(userId, req.totalAmount());
        return OrderResponse.from(orderRepository.save(order));
    }
}
```

---

## 3. Spring Security & Authorization

### SecurityFilterChain Configuration (Stateless JWT)
```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;

    public SecurityConfig(JwtAuthenticationFilter jwtAuthFilter) {
        this.jwtAuthFilter = jwtAuthFilter;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(AbstractHttpConfigurer::disable)
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**", "/actuator/health").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .headers(h -> h.frameOptions(HeadersConfigurer.FrameOptionsConfig::deny))
            .build();
    }
}
```

---

## 4. Test-Driven Development (TDD)

### Unit Testing with JUnit 5 & Mockito
```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock private OrderRepository orderRepository;
    @InjectMocks private OrderService orderService;

    @Test
    void shouldCreateOrderSuccessfully() {
        UUID userId = UUID.randomUUID();
        CreateOrderRequest request = new CreateOrderRequest(new BigDecimal("99.99"));
        Order savedOrder = new Order(userId, new BigDecimal("99.99"));

        when(orderRepository.save(any(Order.class))).thenReturn(savedOrder);

        OrderResponse response = orderService.createOrder(userId, request);

        assertThat(response).isNotNull();
        assertThat(response.totalAmount()).isEqualByComparingTo("99.99");
        verify(orderRepository).save(any(Order.class));
    }
}
```

### Integration Testing with MockMvc & Testcontainers
```java
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class OrderControllerIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired private MockMvc mockMvc;

    @Test
    @WithMockUser(roles = "USER")
    void shouldCreateOrderEndpoint() throws Exception {
        mockMvc.perform(post("/api/v1/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"totalAmount": 49.99}
                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.totalAmount").value(49.99));
    }
}
```

---

## 5. Verification & Pre-Deployment Pipeline

Execute this verification sequence prior to merging PRs:

```bash
# 1. Clean Build & Unit/Integration Tests
./mvnw clean verify -DskipTests=false
# Or Gradle: ./gradlew clean check jacocoTestReport

# 2. Static Code Analysis
./mvnw spotbugs:check pmd:check checkstyle:check

# 3. Security Vulnerability Scanning
./mvnw org.owasp:dependency-check-maven:check

# 4. Production Smoke & Health Check
curl -f http://localhost:8080/actuator/health || exit 1
```
