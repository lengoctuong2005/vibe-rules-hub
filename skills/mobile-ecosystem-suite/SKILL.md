---
name: mobile-ecosystem-suite
description: |
  Master Mobile Ecosystem Suite for production cross-platform and native engineering: React Native (New Architecture, Turbomodules, JSI), Flutter, Swift/SwiftUI, Kotlin/Compose, HarmonyOS/ArkTS, offline-first SQLite bi-directional synchronization, biometric security, and automated multi-agent device farm validation.
triggers:
  - "mobile"
  - "mobile-ecosystem-suite"
  - "react-native"
  - "flutter"
  - "swift"
  - "kotlin"
  - "arkts"
  - "mobile suite"
license: MIT
metadata:
  origin: ECC
---

# Mobile Ecosystem Master Suite

Comprehensive, enterprise-grade mobile development framework spanning cross-platform (React Native, Flutter) and native platform engineering (iOS SwiftUI, Android Jetpack Compose, HarmonyOS ArkTS) with offline-first synchronization and defense-in-depth security.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                        MOBILE PRESENTATION LAYER                        |
|  React Native (Fabric/JSI) · Flutter (Impeller) · SwiftUI · Jetpack · ArkTS |
|  Unidirectional State Flow (Redux / Riverpod / MVI) · 120fps Animations  |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
+──────────────────────────────────┐  +───────────────────────────────────+
|        OFFLINE OUTBOX ENGINE     |  |       LOCAL RELATIONAL STORE      |
|  Optimistic Mutation Queue       |  |  SQLite / Room / SwiftData / ArkTS|
|  Jittered Exponential Retry      |  |  Full-Text Search (FTS5)          |
+─────────────────┬────────────────┘  +─────────────────┬─────────────────+
                  │                                     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                       HARDWARE SECURITY PRIMITIVES                      |
|  iOS Keychain / Secure Enclave · Android KeyStore · Biometrics          |
|  SSL Certificate Pinning · Anti-Tamper & Root Detection                 |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ HTTPS / WSS (Pinning Enforced)
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                       REMOTE CLOUD GATEWAY & SYNC                       |
|  Delta Sync Protocol (Vector Clocks) · WebSocket Push Notifications     |
+─────────────────────────────────────────────────────────────────────────+
```

---

## 2. React Native (New Architecture) & JSI Implementation

```tsx
// src/components/SmoothList.tsx
import React, { useCallback } from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { FlashList } from '@shopify/flash-list';
import Animated, { useAnimatedStyle, withTiming } from 'react-native-reanimated';

interface ItemProps {
  item: { id: string; title: string; subtitle: string };
}

// ponytail: Native-accelerated list item with Reanimated worklet
const ListItem = React.memo(({ item }: ItemProps) => {
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: withTiming(1, { duration: 250 }),
    transform: [{ scale: withTiming(1, { duration: 250 }) }],
  }));

  return (
    <Animated.View style={[styles.card, animatedStyle]}>
      <Text style={styles.title}>{item.title}</Text>
      <Text style={styles.subtitle}>{item.subtitle}</Text>
    </Animated.View>
  );
});

export function SmoothList({ data }: { data: Array<{ id: string; title: string; subtitle: string }> }) {
  const renderItem = useCallback(({ item }: ItemProps) => <ListItem item={item} />, []);

  return (
    <View style={styles.container}>
      <FlashList
        data={data}
        renderItem={renderItem}
        estimatedItemSize={72}
        keyExtractor={(item) => item.id}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0B0F19' },
  card: { padding: 16, marginHorizontal: 16, marginVertical: 6, backgroundColor: '#1A2234', borderRadius: 12 },
  title: { color: '#F3F4F6', fontSize: 16, fontWeight: '600' },
  subtitle: { color: '#9CA3AF', fontSize: 14, marginTop: 4 },
});
```

---

## 3. iOS Native SwiftUI with SwiftData

```swift
// iOS/Sources/Views/NoteListView.swift
import SwiftUI
import SwiftData

@Model
final class NoteItem {
    var id: UUID
    var title: String
    var content: String
    var updatedAt: Date
    var syncPending: Bool

    init(title: String, content: String) {
        self.id = UUID()
        self.title = title
        self.content = content
        self.updatedAt = Date()
        self.syncPending = true
    }
}

struct NoteListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \NoteItem.updatedAt, order: .reverse) private var notes: [NoteItem]

    var body: some View {
        NavigationStack {
            List {
                ForEach(notes) { note in
                    VStack(alignment: .leading, spacing: 4) {
                        Text(note.title)
                            .font(.headline)
                            .foregroundColor(.primary)
                        Text(note.content)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 4)
                }
                .onDelete(perform: deleteNotes)
            }
            .navigationTitle("Master Notes")
        }
    }

    private func deleteNotes(offsets: IndexSet) {
        withAnimation {
            for index in offsets {
                modelContext.delete(notes[index])
            }
        }
    }
}
```

---

## 4. HarmonyOS (ArkTS / ArkUI) Declarative Component

```typescript
// EntryComponent.ets
@Entry
@Component
struct NoteListScreen {
  @State notes: Array<{ id: string, title: string, content: string }> = []
  @State isLoading: boolean = false

  aboutToAppear() {
    this.loadNotesFromLocalDatabase()
  }

  // ponytail: ArkTS direct local query, upgrade to async worker pool when >10k records
  loadNotesFromLocalDatabase() {
    this.isLoading = true
    // Simulated relational local store query
    this.notes = [
      { id: '1', title: 'Architecture Review', content: 'Verify offline delta sync contracts' },
      { id: '2', title: 'Security Audit', content: 'Check certificate pinning hashes' }
    ]
    this.isLoading = false
  }

  build() {
    Column() {
      Text('Master Notes')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor('#FFFFFF')
        .margin({ top: 20, bottom: 12, left: 16 })

      List({ space: 12 }) {
        ForEach(this.notes, (note) => {
          ListItem() {
            Column() {
              Text(note.title)
                .fontSize(16)
                .fontWeight(FontWeight.Medium)
                .fontColor('#F3F4F6')
              Text(note.content)
                .fontSize(14)
                .fontColor('#9CA3AF')
                .margin({ top: 4 })
            }
            .width('100%')
            .padding(16)
            .backgroundColor('#1A2234')
            .borderRadius(12)
          }
        }, (note) => note.id)
      }
      .width('100%')
      .layoutWeight(1)
      .padding({ left: 16, right: 16 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0B0F19')
  }
}
```

---

## 5. Biometric Security & Certificate Pinning

```typescript
// src/security/SecureAuth.ts
import * as Keychain from 'react-native-keychain';

export class SecureAuthService {
  // Store authentication credentials securely in Keychain / KeyStore
  static async storeTokens(accessToken: string, refreshToken: string): Promise<boolean> {
    try {
      await Keychain.setGenericPassword('auth_tokens', JSON.stringify({ accessToken, refreshToken }), {
        accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_ANY_OR_DEVICE_PASSCODE,
        accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
        securityLevel: Keychain.SECURITY_LEVEL.SECURE_HARDWARE,
      });
      return true;
    } catch {
      return false;
    }
  }

  static async retrieveTokens(): Promise<{ accessToken: string; refreshToken: string } | null> {
    try {
      const creds = await Keychain.getGenericPassword({
        authenticationPrompt: { title: 'Authenticate to access your account' },
      });
      if (creds) {
        return JSON.parse(creds.password);
      }
      return null;
    } catch {
      return null;
    }
  }
}
```

---

## 6. Subagent Delegation Matrix

| Subagent | Role & Objective | Invocation Trigger |
|----------|------------------|--------------------|
| `planner` | Screen flows, offline synchronization strategy | Start of new mobile module |
| `architect` | Relational SQLite schema, bi-directional delta protocol | Database or entity updates |
| `tdd-guide` | Red-Green-Refactor state machine tests | Before implementing business logic |
| `mobile-reviewer` | 120fps profiler audit, memory allocations, thread safety | Component or bridge changes |
| `security-reviewer` | Keychain, SSL pinning, ProGuard obfuscation | Before release builds |
| `device-farm-runner` | Maestro / Appium cross-platform automation | Staging and release verification |
