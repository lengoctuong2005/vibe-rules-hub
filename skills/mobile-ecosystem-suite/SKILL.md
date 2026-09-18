---
name: mobile-ecosystem-suite
description: |
  Mobile Ecosystem Master Suite delivering end-to-end mobile architecture across Flutter, React Native, Swift (iOS), and Kotlin (Android). Integrates offline-first SQLite sync engines, hardware-backed encrypted storage, biometric authentication gates, certificate pinning, deep-link protection, and platform-specialized subagents (flutter-reviewer, swift-reviewer, kotlin-reviewer, security-reviewer).
triggers:
  - "mobile"
  - "mobile suite"
  - "mobile-ecosystem-suite"
  - "flutter architecture"
  - "react native"
  - "swift ios"
  - "kotlin android"
  - "offline first mobile"
license: MIT
metadata:
  origin: ECC
---

# Mobile Ecosystem Master Suite

Comprehensive architecture framework for building robust, secure, and offline-first mobile applications across cross-platform and native ecosystems.

---

## 1. Unified Mobile Topology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER                             │
│   Flutter (Widgets) / React Native (JSX) / Swift (SwiftUI) / Compose    │
│   State: BLoC, Riverpod, Zustand, SwiftUI StateObject, StateFlow        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ User Actions
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION / DOMAIN                          │
│   Use Cases + Offline-First Sync Orchestrator                           │
│   Conflict Resolution: LWW (Logical Clocks) / Field CRDTs               │
└──────────────────┬───────────────────────────────────┬──────────────────┘
                   │ Local Mutation                    │ Sync Trigger
                   ▼                                   ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────┐
│            LOCAL STORAGE             │  │       SECURE NETWORKING       │
│  SQLite (Drift/Room/GRDB/Watermelon) │  │  TLS Certificate Pinning      │
│  Encrypted Keychain / Keystore       │  │  Biometric Token Refresh      │
│  Sync Outbox Queue Table             │  │  Universal / App Link Routing │
└──────────────────────────────────────┘  └───────────────────────────────┘
```

---

## 2. Offline-First Synchronization & Conflict Resolution

### Sync Outbox State Machine
1. **PENDING**: Action written locally in SQLite with UUIDv4 and client ISO-8601 timestamp.
2. **IN_FLIGHT**: Outbox worker submits batch payload to backend API.
3. **ACKNOWLEDGED**: Server confirms receipt with server-assigned sequence number; local item removed or marked synced.
4. **CONFLICT**: Server version mismatch triggers Last-Write-Wins or customized merge callback.

```typescript
// ponytail: Minimal Outbox item model - zero external sync library required
export interface SyncOutboxItem {
  id: string;
  entityName: string;
  entityId: string;
  payloadJson: string;
  createdAtUtc: string;
  attempts: number;
}
```

---

## 3. Hardware-Backed Security Protocols

### 1. iOS Keychain Access (Swift)
```swift
// ponytail: Native Keychain wrapper with hardware biometric access control
import Security
import LocalAuthentication

public func saveSecureToken(key: String, data: Data) -> Bool {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: key,
        kSecValueData as String: data,
        kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
    ]
    SecItemDelete(query as CFDictionary)
    return SecItemAdd(query as CFDictionary, nil) == errSecSuccess
}
```

### 2. Android Keystore & EncryptedSharedPreferences (Kotlin)
```kotlin
// ponytail: Hardware-backed EncryptedSharedPreferences using MasterKey AES-256
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val securePreferences = EncryptedSharedPreferences.create(
    context,
    "secret_shared_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```

### 3. Certificate Pinning
Pin public key Subject Public Key Info (`sha256/base64...`) across network clients (Dio, OkHttp, URLSession) to protect against rogue CAs and intercepting proxies.

---

## 4. Platform-Specific Subagent Audit Rules

| Subagent | Key Verification Targets | Fatal Anti-Patterns |
|----------|--------------------------|---------------------|
| `flutter-reviewer` | `const` constructors, `RepaintBoundary` on animations, Stream controller disposal | Unbounded `setState()` in list items, memory leaks in image caching |
| `swift-reviewer` | Swift 6 strict concurrency (`@Sendable`), memory safety (`[weak self]`) | Retain cycles in async closures, non-MainActor UI mutations |
| `kotlin-reviewer` | Jetpack Compose `remember` / `derivedStateOf`, Coroutine scopes | Leaking `CoroutineScope` beyond ViewModel lifecycle, blocking dispatcher |
| `security-reviewer` | Certificate pinning active, biometric fallbacks guarded, deep-links whitelisted | Storing plaintext tokens in AsyncStorage / UserDefaults, missing cert pins |

---

## 5. Verification Checklist

```bash
# 1. Static Analysis & Lint
flutter analyze          # For Flutter
pnpm tsc --noEmit        # For React Native
swiftlint                # For iOS
./gradlew lint           # For Android

# 2. Offline Sync & Unit Tests
flutter test / ./gradlew test

# 3. Secret scan
python scripts/safety_guard.py --scan-file .
```
