---
name: laravel
description: |
  Comprehensive enterprise Laravel suite covering Architectural Patterns (Action/Service layers, Routing, Form Requests), Eloquent ORM Optimization, Queues/Events/Jobs, Package Discovery (LaraPlugins MCP), Security Hardening (Sanctum, Policies, Mass Assignment, CSRF), Test-Driven Development (Pest/PHPUnit, Factories, HTTP Feature tests), and Verification/Pre-Deployment Gates.
triggers:
  - "laravel"
  - "eloquent"
  - "artisan"
  - "laravel security"
  - "laravel tdd"
  - "pest php"
  - "sanctum"
  - "laravel patterns"
  - "laraplugins"
license: MIT
metadata:
  origin: ECC
---

# Laravel Enterprise Development Suite

Production-grade engineering guide for building, securing, testing, and optimizing modern PHP Laravel applications.

---

## 1. Architecture & Action-Driven Structure

### Recommended Directory Layout
```
app/
├── Actions/              # Single-purpose invocable domain actions
├── Http/
│   ├── Controllers/      # Thin controllers delegating to Actions/Services
│   ├── Requests/         # Form request validation
│   └── Resources/        # API Resource JSON transformers
├── Models/               # Typed Eloquent models & casts
├── Jobs/                 # Queueable async jobs
└── Policies/             # Granular authorization policies
```

### Thin Controllers & Invocable Actions
```php
namespace App\Actions\Orders;

use App\Models\Order;
use App\Models\User;
use Illuminate\Support\Facades\DB;

class CreateOrderAction
{
    public function execute(User $user, array $orderData): Order
    {
        return DB::transaction(function () use ($user, $orderData) {
            $order = $user->orders()->create([
                'status' => 'pending',
                'total_cents' => $orderData['total_cents'],
            ]);

            $order->items()->createMany($orderData['items']);
            return $order;
        });
    }
}
```

```php
namespace App\Http\Controllers;

use App\Actions\Orders\CreateOrderAction;
use App\Http\Requests\CreateOrderRequest;
use App\Http\Resources\OrderResource;

class OrderController extends Controller
{
    public function store(CreateOrderRequest $request, CreateOrderAction $createOrder)
    {
        $order = $createOrder->execute($request->user(), $request->validated());
        return new OrderResource($order);
    }
}
```

---

## 2. Eloquent ORM & Query Optimization

### Eliminating N+1 Queries with Eager Loading
```php
// Eager load single and nested relations
$orders = Order::with(['user', 'items.product'])->paginate(20);

// Lazy eager loading on existing collections
$orders->loadMissing('shippingAddress');

// Constrained eager loading
$users = User::with(['orders' => function ($query) {
    $query->where('status', 'completed')->latest()->limit(5);
}])->get();
```

### Strict Mass Assignment & Attribute Casting
```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Casts\Attribute;

class Order extends Model
{
    // Protect against mass assignment vulnerability
    protected $fillable = ['status', 'total_cents', 'shipping_address'];

    // Native attribute casting
    protected function casts(): array
    {
        return [
            'total_cents' => 'integer',
            'paid_at' => 'datetime',
            'metadata' => 'encrypted:array',
        ];
    }
}
```

---

## 3. Package Discovery via LaraPlugins MCP

Check package health, security, and version compatibility before adding dependencies:

```json
// ~/.claude.json mcpServers:
"laraplugins": {
  "type": "http",
  "url": "https://laraplugins.io/mcp/plugins"
}
```

- Discover verified packages: `search_plugin({ query: "auth sanctum", min_health_score: 80 })`
- Evaluate maintenance and compatibility: `get_plugin_details({ package_name: "spatie/laravel-permission" })`

---

## 4. Security Hardening & Authorization

### Environment Security & Secret Keys
```php
// config/app.php
'env' => env('APP_ENV', 'production'),
'debug' => (bool) env('APP_DEBUG', false), // MUST be false in production
'key' => env('APP_KEY'),

// config/session.php
'secure' => env('SESSION_SECURE_COOKIE', true),
'http_only' => true,
'same_site' => 'lax',
```

### API Authentication (Sanctum) & Granular Policies
```php
namespace App\Policies;

use App\Models\Order;
use App\Models\User;

class OrderPolicy
{
    public function view(User $user, Order $order): bool
    {
        return $user->id === $order->user_id || $user->tokenCan('orders:read-all');
    }
}
```

```php
// In Controller or FormRequest:
$this->authorize('view', $order);
```

### SQL Injection Prevention
```php
// NEVER: DB::raw("SELECT * FROM orders WHERE status = '" . $status . "'");
// ALWAYS: Parameterized bindings
DB::select("SELECT * FROM orders WHERE status = ?", [$status]);
```

---

## 5. Test-Driven Development (Pest & PHPUnit)

### Feature Test with Pest
```php
use App\Models\User;
use App\Models\Order;
use function Pest\Laravel\actingAs;
use function Pest\Laravel\assertDatabaseHas;
use function Pest\Laravel\postJson;

it('creates an order for authenticated user', function () {
    $user = User::factory()->create();

    actingAs($user)
        ->postJson('/api/orders', [
            'total_cents' => 4999,
            'items' => [
                ['product_id' => 1, 'quantity' => 2, 'unit_price_cents' => 2500]
            ]
        ])
        ->assertCreated()
        ->assertJsonPath('data.status', 'pending');

    assertDatabaseHas('orders', [
        'user_id' => $user->id,
        'total_cents' => 4999,
    ]);
});
```

---

## 6. Verification & Pre-Deployment Gates

Execute before PR merge or production deployment:

```bash
# 1. Environment & Config Verification
php artisan config:clear
php artisan env

# 2. Static Analysis & Code Style
./vendor/bin/pint --test
./vendor/bin/phpstan analyse --level=8

# 3. Test Suite & Coverage (>= 80%)
./vendor/bin/pest --coverage --min=80

# 4. Security & Package Audits
composer audit
php artisan security:check

# 5. Production Optimization Caches
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan event:cache
```
