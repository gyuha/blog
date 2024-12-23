---
title: "유용한 Aspect-Oriented Programming(AOP) 모음"
date: 2024-12-20T13:15:31+09:00
draft: true
categories: ["Spring"]
tags: ["Spring", "annotation"]
---

Aspect-Oriented Programming(AOP)은 Spring에서 횡단 관심사를 처리하기 위한 강력한 도구입니다. 
<!--more-->
AOP를 활용하면 애플리케이션의 주요 비즈니스 로직을 간결하게 유지하면서도, 반복적인 작업을 쉽게 처리할 수 있습니다. 아래는 Spring AOP를 활용해 구현할 수 있는 몇 가지 유용한 기능과 구현 예제입니다.

---

## **1. 로깅 (Logging)**  
메서드의 입력값, 출력값, 실행 시간을 로깅하는 기능.

**구현 예제**  
```java
@Aspect
@Component
public class LoggingAspect {

    @Around("execution(* com.example..*(..))") // com.example 패키지의 모든 메서드
    public Object logMethodDetails(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Method " + joinPoint.getSignature() + " called with args: " + Arrays.toString(joinPoint.getArgs()));
        Object result = joinPoint.proceed();
        System.out.println("Method " + joinPoint.getSignature() + " returned: " + result);
        return result;
    }
}
```

---

## **2. 보안 검사 (Security Check)**  
메서드 실행 전 사용자의 인증 및 권한을 검사하는 기능.

**구현 예제**  
```java
@Aspect
@Component
public class SecurityAspect {

    @Before("@annotation(com.example.annotations.SecureAction)") // 특정 어노테이션이 붙은 메서드만
    public void checkSecurity() {
        // 예: 현재 사용자의 권한을 확인
        boolean hasPermission = SecurityContextHolder.getContext().getAuthentication().isAuthenticated();
        if (!hasPermission) {
            throw new SecurityException("User not authorized!");
        }
        System.out.println("User is authorized");
    }
}
```

---

## **3. 트랜잭션 관리 (Custom Transaction Management)**  
Spring의 기본 트랜잭션 외에, 특정 작업에서 커스텀 트랜잭션 처리를 추가.

**구현 예제**  
```java
@Aspect
@Component
public class TransactionManagementAspect {

    @Around("@annotation(org.springframework.transaction.annotation.Transactional)")
    public Object manageTransaction(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Transaction started");
        try {
            Object result = joinPoint.proceed();
            System.out.println("Transaction committed");
            return result;
        } catch (Exception ex) {
            System.out.println("Transaction rolled back");
            throw ex;
        }
    }
}
```

---

## **4. 캐싱 (Caching)**  
결과를 캐싱하여 메서드 호출을 최적화.

**구현 예제**  
```java
@Aspect
@Component
public class CachingAspect {

    private final Map<String, Object> cache = new HashMap<>();

    @Around("@annotation(com.example.annotations.Cached)")
    public Object cacheResult(ProceedingJoinPoint joinPoint) throws Throwable {
        String key = joinPoint.getSignature().toString() + Arrays.toString(joinPoint.getArgs());
        if (cache.containsKey(key)) {
            System.out.println("Cache hit for key: " + key);
            return cache.get(key);
        }
        System.out.println("Cache miss for key: " + key);
        Object result = joinPoint.proceed();
        cache.put(key, result);
        return result;
    }
}
```

---

## **5. 예외 처리 (Global Exception Handling)**  
특정 패키지의 메서드에서 발생한 예외를 중앙에서 처리.

**구현 예제**  
```java
@Aspect
@Component
public class ExceptionHandlingAspect {

    @AfterThrowing(pointcut = "execution(* com.example..*(..))", throwing = "ex")
    public void handleException(JoinPoint joinPoint, Exception ex) {
        System.err.println("Exception in method " + joinPoint.getSignature() + ": " + ex.getMessage());
        // 로그 저장 또는 알림 전송
    }
}
```

---

## **6. 메트릭 수집 (Metrics Collection)**  
메서드 호출 횟수, 평균 실행 시간을 수집하여 성능 모니터링.

**구현 예제**  
```java
@Aspect
@Component
public class MetricsAspect {

    private final Map<String, Long> executionCount = new HashMap<>();
    private final Map<String, Long> totalTime = new HashMap<>();

    @Around("execution(* com.example..*(..))")
    public Object collectMetrics(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().toString();
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;

        executionCount.put(methodName, executionCount.getOrDefault(methodName, 0L) + 1);
        totalTime.put(methodName, totalTime.getOrDefault(methodName, 0L) + duration);

        System.out.println("Method " + methodName + " called " + executionCount.get(methodName) + " times");
        System.out.println("Average execution time: " + (totalTime.get(methodName) / executionCount.get(methodName)) + " ms");

        return result;
    }
}
```

---

## **7. 입력값 검증 (Validation)**  
메서드 호출 전에 입력값이 유효한지 검증.

**구현 예제**  
```java
@Aspect
@Component
public class ValidationAspect {

    @Before("@annotation(com.example.annotations.ValidateInput)")
    public void validateInputs(JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs();
        for (Object arg : args) {
            if (arg == null) {
                throw new IllegalArgumentException("Null value not allowed for arguments!");
            }
        }
        System.out.println("All inputs are valid");
    }
}
```
여기에는 Spring AOP를 활용하여 더 다양한 유용한 기능을 구현한 예제를 소개합니다. 각 기능은 프로젝트에 따라 확장 가능하며, 비즈니스 요구사항에 따라 활용될 수 있습니다.

---

## **8. 요청 데이터 암호화 및 복호화**  
API 요청 데이터나 응답 데이터를 암호화/복호화하여 보안성을 강화.

**구현 예제**  
```java
@Aspect
@Component
public class EncryptionAspect {

    private static final String SECRET_KEY = "my-secret-key";

    @Around("@annotation(com.example.annotations.EncryptData)")
    public Object encryptAndDecrypt(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        
        // 암호화된 데이터로 변경
        for (int i = 0; i < args.length; i++) {
            if (args[i] instanceof String) {
                args[i] = encrypt((String) args[i]);
            }
        }
        System.out.println("Arguments encrypted: " + Arrays.toString(args));

        // 메서드 실행
        Object result = joinPoint.proceed(args);

        // 복호화된 결과 반환
        if (result instanceof String) {
            result = decrypt((String) result);
            System.out.println("Result decrypted: " + result);
        }

        return result;
    }

    private String encrypt(String data) {
        // 간단한 암호화 로직 (예시)
        return Base64.getEncoder().encodeToString((data + SECRET_KEY).getBytes());
    }

    private String decrypt(String data) {
        // 간단한 복호화 로직 (예시)
        String decoded = new String(Base64.getDecoder().decode(data));
        return decoded.replace(SECRET_KEY, "");
    }
}
```

---

## **9. API 호출 제한 (Rate Limiting)**  
특정 사용자가 API를 과도하게 호출하지 않도록 제한.

**구현 예제**  
```java
@Aspect
@Component
public class RateLimitingAspect {

    private final Map<String, Integer> userRequestCounts = new HashMap<>();
    private static final int LIMIT = 5; // 요청 제한

    @Before("@annotation(com.example.annotations.RateLimited)")
    public void enforceRateLimit(JoinPoint joinPoint) {
        String userId = getCurrentUserId(); // 사용자 ID 가져오기 (가정)

        userRequestCounts.put(userId, userRequestCounts.getOrDefault(userId, 0) + 1);

        if (userRequestCounts.get(userId) > LIMIT) {
            throw new RuntimeException("Rate limit exceeded for user: " + userId);
        }
        System.out.println("Request allowed for user: " + userId);
    }

    private String getCurrentUserId() {
        // 현재 사용자 ID를 가져오는 로직 (예: 보안 컨텍스트)
        return "user123";
    }
}
```

---

## **10. 메서드 리트라이 (Retry)**  
실패한 메서드 호출을 일정 횟수까지 재시도.

**구현 예제**  
```java
@Aspect
@Component
public class RetryAspect {

    @Around("@annotation(com.example.annotations.Retryable)")
    public Object retry(ProceedingJoinPoint joinPoint) throws Throwable {
        int maxRetries = 3; // 최대 재시도 횟수
        int attempts = 0;

        while (true) {
            try {
                return joinPoint.proceed(); // 메서드 실행
            } catch (Exception ex) {
                attempts++;
                System.out.println("Attempt " + attempts + " failed");
                if (attempts >= maxRetries) {
                    System.out.println("Max retries reached");
                    throw ex;
                }
            }
        }
    }
}
```

---

## **11. 감사 로깅 (Audit Logging)**  
중요한 작업(예: 데이터베이스 변경)을 기록하여 감사를 가능하게 함.

**구현 예제**  
```java
@Aspect
@Component
public class AuditLoggingAspect {

    @After("@annotation(com.example.annotations.AuditLog)")
    public void logAuditDetails(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        String userName = getCurrentUserName(); // 현재 사용자 가져오기 (가정)
        System.out.println("User " + userName + " executed " + methodName);
        // 로그 저장 또는 DB에 기록
    }

    private String getCurrentUserName() {
        // 현재 사용자 이름을 반환 (예: 보안 컨텍스트)
        return "admin";
    }
}
```

---

## **12. 메서드 호출 알림 (Notification)**  
특정 메서드가 호출되었을 때 알림을 전송.

**구현 예제**  
```java
@Aspect
@Component
public class NotificationAspect {

    @After("@annotation(com.example.annotations.NotifyOnCall)")
    public void sendNotification(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        System.out.println("Notification: Method " + methodName + " was called");
        // 알림 전송 (예: 이메일, SMS, 슬랙)
    }
}
```

---

## **13. 요청 추적 (Request Tracing)**  
모든 요청을 추적하여 디버깅 및 모니터링.

**구현 예제**  
```java
@Aspect
@Component
public class RequestTracingAspect {

    @Before("execution(* com.example.controller..*(..))") // 컨트롤러의 모든 메서드
    public void traceRequest(JoinPoint joinPoint) {
        System.out.println("Request received for method: " + joinPoint.getSignature());
        System.out.println("Arguments: " + Arrays.toString(joinPoint.getArgs()));
    }
}
```

---

## **14. 데이터 변경 이벤트 처리**  
데이터 변경 시 추가 작업(예: 캐시 무효화) 수행.

**구현 예제**  
```java
@Aspect
@Component
public class DataChangeAspect {

    @AfterReturning("@annotation(com.example.annotations.OnDataChange)")
    public void handleDataChange(JoinPoint joinPoint) {
        System.out.println("Data change detected in method: " + joinPoint.getSignature());
        // 캐시 무효화, 이벤트 전송 등의 작업 수행
    }
}
```

---

## **15. 성능 문제 감지 (Performance Monitoring)**  
특정 메서드에서 일정 시간을 초과하는 경우 경고를 출력.

**구현 예제**  
```java
@Aspect
@Component
public class PerformanceMonitoringAspect {

    private static final long WARNING_THRESHOLD = 1000; // 1초

    @Around("@annotation(com.example.annotations.MonitorPerformance)")
    public Object monitorPerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;

        if (duration > WARNING_THRESHOLD) {
            System.err.println("Performance warning: " + joinPoint.getSignature() + " took " + duration + " ms");
        } else {
            System.out.println(joinPoint.getSignature() + " executed in " + duration + " ms");
        }

        return result;
    }
}
```

---

## **16. 데이터베이스 슬로우 쿼리 탐지**  
SQL 실행 시간이 긴 경우 경고 로그를 남기거나 알림을 보냅니다.

**구현 예제**  
```java
@Aspect
@Component
public class SlowQueryDetectorAspect {

    private static final long SLOW_QUERY_THRESHOLD = 2000; // 2초

    @Around("execution(* com.example.repository..*(..))") // Repository 계층 감시
    public Object detectSlowQueries(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;

        if (duration > SLOW_QUERY_THRESHOLD) {
            System.err.println("Slow query detected: " + joinPoint.getSignature() + " took " + duration + " ms");
        }

        return result;
    }
}
```

---

## **17. 사용자 접근 로그 기록 (Access Logging)**  
API 호출 시 사용자의 IP 주소, 요청 시간 등을 기록합니다.

**구현 예제**  
```java
@Aspect
@Component
public class AccessLoggingAspect {

    @Before("execution(* com.example.controller..*(..))") // 모든 컨트롤러 메서드
    public void logAccess(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        String ipAddress = getClientIp(); // 클라이언트 IP 가져오기
        System.out.println("Access log: " + methodName + " called from IP: " + ipAddress);
    }

    private String getClientIp() {
        // HttpServletRequest를 통해 IP 주소 가져오기
        return "127.0.0.1"; // 예제용
    }
}
```

---

## **18. 조건부 실행 (Conditional Execution)**  
특정 조건에서만 메서드를 실행하거나 무시합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ConditionalExecutionAspect {

    @Around("@annotation(com.example.annotations.ConditionalRun)")
    public Object executeConditionally(ProceedingJoinPoint joinPoint) throws Throwable {
        boolean shouldRun = checkCondition(); // 실행 조건 확인
        if (shouldRun) {
            return joinPoint.proceed(); // 조건이 충족되면 실행
        } else {
            System.out.println("Method " + joinPoint.getSignature() + " skipped due to condition");
            return null; // 실행하지 않음
        }
    }

    private boolean checkCondition() {
        // 조건 로직 (예: 특정 설정값 확인)
        return false;
    }
}
```

---

## **19. 메서드 호출 수 제한**  
특정 메서드가 지정된 횟수 이상 호출되지 않도록 제한합니다.

**구현 예제**  
```java
@Aspect
@Component
public class MethodCallLimiterAspect {

    private final Map<String, Integer> methodCallCounts = new HashMap<>();
    private static final int MAX_CALLS = 10; // 최대 호출 횟수

    @Before("@annotation(com.example.annotations.LimitedCall)")
    public void limitMethodCalls(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        int currentCount = methodCallCounts.getOrDefault(methodName, 0);

        if (currentCount >= MAX_CALLS) {
            throw new RuntimeException("Method " + methodName + " has been called too many times");
        }

        methodCallCounts.put(methodName, currentCount + 1);
        System.out.println("Method " + methodName + " called " + (currentCount + 1) + " times");
    }
}
```

---

## **20. 사용자 ID 태깅 (User ID Tagging)**  
로그나 메트릭에 현재 사용자 ID를 태깅하여 사용자별 모니터링을 제공합니다.

**구현 예제**  
```java
@Aspect
@Component
public class UserIdTaggingAspect {

    @Before("execution(* com.example.service..*(..))") // 서비스 계층 메서드 감시
    public void tagUserId(JoinPoint joinPoint) {
        String userId = getCurrentUserId(); // 현재 사용자 ID 가져오기
        System.out.println("Tagging user ID: " + userId + " for method: " + joinPoint.getSignature());
    }

    private String getCurrentUserId() {
        // 보안 컨텍스트에서 사용자 ID 가져오기
        return "user123"; // 예제용
    }
}
```

---

## **21. 필드 마스킹 (Field Masking)**  
로그 출력 시 민감한 데이터를 마스킹합니다.

**구현 예제**  
```java
@Aspect
@Component
public class FieldMaskingAspect {

    @Around("execution(* com.example.service..*(..))") // 서비스 계층 메서드 감시
    public Object maskSensitiveFields(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = joinPoint.proceed();
        if (result instanceof String) {
            // 민감한 데이터 마스킹 (예: 이메일, 카드 번호)
            result = ((String) result).replaceAll("(?<=.{2}).(?=.*@)", "*");
        }
        return result;
    }
}
```

---

## **22. 실행 환경 확인 (Environment Check)**  
테스트 환경이나 프로덕션 환경에 따라 다른 동작을 수행.

**구현 예제**  
```java
@Aspect
@Component
public class EnvironmentCheckAspect {

    @Around("@annotation(com.example.annotations.EnvironmentSensitive)")
    public Object checkEnvironment(ProceedingJoinPoint joinPoint) throws Throwable {
        String currentEnv = getCurrentEnvironment(); // 현재 환경 가져오기
        if ("prod".equals(currentEnv)) {
            System.out.println("Executing in production");
        } else {
            System.out.println("Executing in non-production environment");
        }
        return joinPoint.proceed();
    }

    private String getCurrentEnvironment() {
        // Spring Environment에서 현재 프로파일 가져오기
        return "dev"; // 예제용
    }
}
```

---

## **23. 특정 패키지 메서드 호출 차단**  
특정 패키지의 메서드가 호출되지 않도록 차단합니다.

**구현 예제**  
```java
@Aspect
@Component
public class MethodBlockingAspect {

    @Before("execution(* com.example.unallowed..*(..))") // 금지된 패키지
    public void blockMethodCall(JoinPoint joinPoint) {
        throw new RuntimeException("Method " + joinPoint.getSignature() + " is not allowed to be called");
    }
}
```

---

## **24. 메서드 입력값 변환 (Input Transformation)**  
메서드 호출 전에 입력값을 변환.

**구현 예제**  
```java
@Aspect
@Component
public class InputTransformationAspect {

    @Around("@annotation(com.example.annotations.TransformInput)")
    public Object transformInput(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();

        for (int i = 0; i < args.length; i++) {
            if (args[i] instanceof String) {
                args[i] = ((String) args[i]).toUpperCase(); // 입력값 대문자 변환
            }
        }
        System.out.println("Transformed arguments: " + Arrays.toString(args));

        return joinPoint.proceed(args);
    }
}
```

---

## **25. 메모리 사용 모니터링 (Memory Usage Monitoring)**  
메서드 실행 전후로 메모리 사용량을 기록.

**구현 예제**  
```java
@Aspect
@Component
public class MemoryMonitoringAspect {

    @Around("@annotation(com.example.annotations.MonitorMemory)")
    public Object monitorMemoryUsage(ProceedingJoinPoint joinPoint) throws Throwable {
        Runtime runtime = Runtime.getRuntime();
        long beforeMemory = runtime.totalMemory() - runtime.freeMemory();

        Object result = joinPoint.proceed();

        long afterMemory = runtime.totalMemory() - runtime.freeMemory();
        System.out.println("Memory usage for method " + joinPoint.getSignature() + ": " + (afterMemory - beforeMemory) + " bytes");

        return result;
    }
}
```

---

## **26. API 요청 제한 속도 조정 (Dynamic Throttling)**  
시스템 상태나 사용자 그룹에 따라 요청 속도를 동적으로 제한합니다.

**구현 예제**  
```java
@Aspect
@Component
public class DynamicThrottlingAspect {

    private final Map<String, Long> userLastRequestTime = new HashMap<>();
    private static final long MIN_INTERVAL = 1000; // 최소 요청 간격 (1초)

    @Before("@annotation(com.example.annotations.Throttled)")
    public void enforceThrottling(JoinPoint joinPoint) {
        String userId = getCurrentUserId(); // 사용자 ID 가져오기
        long currentTime = System.currentTimeMillis();

        if (userLastRequestTime.containsKey(userId)) {
            long lastRequestTime = userLastRequestTime.get(userId);
            if (currentTime - lastRequestTime < MIN_INTERVAL) {
                throw new RuntimeException("Too many requests for user: " + userId);
            }
        }

        userLastRequestTime.put(userId, currentTime);
    }

    private String getCurrentUserId() {
        // 예: 보안 컨텍스트에서 사용자 ID 가져오기
        return "user123"; // 예제용
    }
}
```

---

## **27. 컨트롤러 응답 변환 (Response Transformation)**  
컨트롤러의 반환값을 동적으로 수정하여 사용자 맞춤 데이터를 반환합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ResponseTransformationAspect {

    @AfterReturning(pointcut = "execution(* com.example.controller..*(..))", returning = "response")
    public Object transformResponse(JoinPoint joinPoint, Object response) {
        if (response instanceof String) {
            return ((String) response).toUpperCase(); // 응답을 대문자로 변환
        }
        return response;
    }
}
```

---

## **28. 실시간 메트릭 수집 (Real-time Metrics Collection)**  
메서드 실행 데이터를 외부 모니터링 시스템으로 전송합니다.

**구현 예제**  
```java
@Aspect
@Component
public class RealTimeMetricsAspect {

    @AfterReturning("execution(* com.example.service..*(..))")
    public void sendMetricsToSystem(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        System.out.println("Sending execution metrics for: " + methodName);
        // 외부 시스템에 메트릭 전송 (예: Prometheus, DataDog)
    }
}
```

---

## **29. 사용자별 데이터 필터링**  
사용자 권한에 따라 반환되는 데이터를 필터링합니다.

**구현 예제**  
```java
@Aspect
@Component
public class DataFilteringAspect {

    @Around("execution(* com.example.service..*(..)) && @annotation(com.example.annotations.FilteredData)")
    public Object filterDataForUser(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = joinPoint.proceed();

        // 사용자 권한에 따른 데이터 필터링
        if (result instanceof List) {
            List<?> list = (List<?>) result;
            return list.stream()
                    .filter(item -> userHasAccess(item)) // 사용자 접근 권한 필터
                    .toList();
        }
        return result;
    }

    private boolean userHasAccess(Object item) {
        // 접근 권한 로직
        return true; // 예제용
    }
}
```

---

## **30. 메서드 파라미터 로그 제외 (Sensitive Logging)**  
특정 파라미터를 로그에서 제외하여 민감 정보를 보호합니다.

**구현 예제**  
```java
@Aspect
@Component
public class SensitiveLoggingAspect {

    @Around("execution(* com.example.service..*(..))")
    public Object excludeSensitiveParams(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        String methodName = joinPoint.getSignature().toShortString();

        // 민감 데이터 마스킹
        Object[] sanitizedArgs = Arrays.stream(args)
                .map(arg -> arg instanceof String && isSensitive(arg) ? "****" : arg)
                .toArray();

        System.out.println("Method " + methodName + " called with args: " + Arrays.toString(sanitizedArgs));
        return joinPoint.proceed();
    }

    private boolean isSensitive(Object arg) {
        // 민감 정보 판별 (예: 비밀번호, 카드 번호)
        return arg.toString().matches(".*\\d{4}-\\d{4}-\\d{4}-\\d{4}.*"); // 카드 번호 예시
    }
}
```

---

## **31. 백그라운드 태스크 실행 (Background Task Execution)**  
메서드 실행을 비동기로 처리하여 응답 속도를 높입니다.

**구현 예제**  
```java
@Aspect
@Component
public class BackgroundTaskAspect {

    private final ExecutorService executorService = Executors.newCachedThreadPool();

    @Around("@annotation(com.example.annotations.BackgroundTask)")
    public void executeInBackground(ProceedingJoinPoint joinPoint) {
        executorService.submit(() -> {
            try {
                joinPoint.proceed();
                System.out.println("Executed in background: " + joinPoint.getSignature());
            } catch (Throwable e) {
                e.printStackTrace();
            }
        });
    }
}
```

---

## **32. 디버그 모드 활성화 (Debug Mode Toggle)**  
애플리케이션의 디버그 모드에서만 특정 로직을 실행합니다.

**구현 예제**  
```java
@Aspect
@Component
public class DebugModeAspect {

    private static final boolean DEBUG_MODE = true; // 설정에 따라 변경 가능

    @Around("@annotation(com.example.annotations.DebugOnly)")
    public Object executeInDebugMode(ProceedingJoinPoint joinPoint) throws Throwable {
        if (DEBUG_MODE) {
            System.out.println("Debug mode enabled for method: " + joinPoint.getSignature());
            return joinPoint.proceed();
        } else {
            System.out.println("Debug mode skipped for method: " + joinPoint.getSignature());
            return null; // 디버그 모드가 아니면 실행 생략
        }
    }
}
```

---

## **33. 캐시 삭제 후처리 (Post Cache Eviction Handling)**  
캐시 삭제 후 추가 작업을 처리합니다.

**구현 예제**  
```java
@Aspect
@Component
public class PostCacheEvictionAspect {

    @After("@annotation(org.springframework.cache.annotation.CacheEvict)")
    public void handleCacheEviction(JoinPoint joinPoint) {
        System.out.println("Cache evicted for method: " + joinPoint.getSignature());
        // 캐시 삭제 후 작업 (예: 로깅, 알림)
    }
}
```

---

## **34. 데이터 통합 검증 (Unified Data Validation)**  
모든 데이터 입력에 대해 통합적으로 검증을 수행합니다.

**구현 예제**  
```java
@Aspect
@Component
public class UnifiedValidationAspect {

    @Before("execution(* com.example.controller..*(..))")
    public void validateData(JoinPoint joinPoint) {
        for (Object arg : joinPoint.getArgs()) {
            if (!isValid(arg)) {
                throw new IllegalArgumentException("Invalid argument: " + arg);
            }
        }
        System.out.println("All arguments are valid for method: " + joinPoint.getSignature());
    }

    private boolean isValid(Object arg) {
        // 데이터 유효성 검사 로직
        return arg != null; // 예제용
    }
}
```

---

## **35. 조건부 트랜잭션 관리 (Conditional Transaction Management)**  
특정 조건에서만 트랜잭션을 활성화합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ConditionalTransactionAspect {

    @Around("@annotation(org.springframework.transaction.annotation.Transactional)")
    public Object manageTransactionConditionally(ProceedingJoinPoint joinPoint) throws Throwable {
        if (shouldActivateTransaction()) {
            System.out.println("Transaction started for: " + joinPoint.getSignature());
            Object result = joinPoint.proceed();
            System.out.println("Transaction committed for: " + joinPoint.getSignature());
            return result;
        } else {
            System.out.println("Transaction skipped for: " + joinPoint.getSignature());
            return joinPoint.proceed();
        }
    }

    private boolean shouldActivateTransaction() {
        // 트랜잭션 활성화 조건
        return true; // 예제용
    }
}
```

---

## **36. 데이터 변경 알림 (Change Notification)**  
특정 데이터가 변경되었을 때 관리자에게 알림을 전송합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ChangeNotificationAspect {

    @AfterReturning("@annotation(com.example.annotations.NotifyChange)")
    public void notifyOnChange(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        System.out.println("Data change detected in method: " + methodName);
        sendNotification("Data has been changed in " + methodName);
    }

    private void sendNotification(String message) {
        // 이메일 또는 SMS 전송 로직
        System.out.println("Notification sent: " + message);
    }
}
```

---

## **37. 캐시 프리로드 (Cache Preloading)**  
애플리케이션 시작 시 특정 데이터를 캐시에 미리 로드합니다.

**구현 예제**  
```java
@Aspect
@Component
public class CachePreloadingAspect {

    @PostConstruct // 애플리케이션 시작 시 호출
    public void preloadCache() {
        System.out.println("Preloading cache...");
        // 캐시 초기화 로직
        loadCache("key1", "value1");
        loadCache("key2", "value2");
    }

    private void loadCache(String key, String value) {
        // 캐시에 데이터 로드
        System.out.println("Cached: " + key + " -> " + value);
    }
}
```

---

## **38. 특정 메서드 비활성화 (Method Deactivation)**  
관리자가 지정한 메서드를 비활성화하여 호출되지 않도록 합니다.

**구현 예제**  
```java
@Aspect
@Component
public class MethodDeactivationAspect {

    private static final Set<String> deactivatedMethods = Set.of("com.example.service.MyService.deactivatedMethod");

    @Before("execution(* com.example..*(..))")
    public void blockDeactivatedMethods(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toString();
        if (deactivatedMethods.contains(methodName)) {
            throw new RuntimeException("Method " + methodName + " is currently deactivated");
        }
    }
}
```

---

## **39. API 요청 경로 추적 (Request Path Tracing)**  
모든 HTTP 요청의 경로를 추적하여 디버깅 정보를 출력합니다.

**구현 예제**  
```java
@Aspect
@Component
public class RequestPathTracingAspect {

    @Before("execution(* org.springframework.web.bind.annotation.RestController..*(..))")
    public void traceRequestPath(JoinPoint joinPoint) {
        String path = joinPoint.getSignature().toShortString();
        System.out.println("Request received for path: " + path);
    }
}
```

---

## **40. 메서드 병렬 실행 (Parallel Execution)**  
특정 메서드를 병렬로 실행하여 성능을 높입니다.

**구현 예제**  
```java
@Aspect
@Component
public class ParallelExecutionAspect {

    private final ExecutorService executor = Executors.newFixedThreadPool(10);

    @Around("@annotation(com.example.annotations.ParallelExecution)")
    public Object executeInParallel(ProceedingJoinPoint joinPoint) {
        executor.submit(() -> {
            try {
                joinPoint.proceed();
                System.out.println("Executed in parallel: " + joinPoint.getSignature());
            } catch (Throwable e) {
                e.printStackTrace();
            }
        });
        return null; // 병렬 실행이므로 결과를 즉시 반환
    }
}
```

---

## **41. 결과 데이터 포맷팅 (Result Formatting)**  
메서드 반환값을 JSON이나 XML 등 특정 형식으로 변환합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ResultFormattingAspect {

    @AfterReturning(pointcut = "@annotation(com.example.annotations.FormatResult)", returning = "result")
    public Object formatResult(JoinPoint joinPoint, Object result) {
        if (result != null) {
            // JSON 형식으로 변환
            String jsonResult = toJson(result);
            System.out.println("Formatted result: " + jsonResult);
            return jsonResult;
        }
        return result;
    }

    private String toJson(Object result) {
        // 간단한 JSON 변환 로직
        return "{\"data\": \"" + result.toString() + "\"}";
    }
}
```

---

## **42. 실행 결과 캐싱 (Result Caching)**  
메서드 실행 결과를 캐싱하여 동일한 요청에 대해 재사용합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ResultCachingAspect {

    private final Map<String, Object> cache = new HashMap<>();

    @Around("@annotation(com.example.annotations.Cacheable)")
    public Object cacheResult(ProceedingJoinPoint joinPoint) throws Throwable {
        String key = generateCacheKey(joinPoint);

        if (cache.containsKey(key)) {
            System.out.println("Cache hit for key: " + key);
            return cache.get(key);
        }

        Object result = joinPoint.proceed();
        cache.put(key, result);
        System.out.println("Cache saved for key: " + key);
        return result;
    }

    private String generateCacheKey(ProceedingJoinPoint joinPoint) {
        return joinPoint.getSignature().toString() + Arrays.toString(joinPoint.getArgs());
    }
}
```

---

## **43. 요청의 IP 블랙리스트 처리 (IP Blacklisting)**  
특정 IP 주소에서의 요청을 차단합니다.

**구현 예제**  
```java
@Aspect
@Component
public class IPBlacklistAspect {

    private static final Set<String> blacklistedIPs = Set.of("192.168.0.1", "10.0.0.1");

    @Before("execution(* com.example.controller..*(..))")
    public void blockBlacklistedIPs() {
        String clientIp = getClientIP();
        if (blacklistedIPs.contains(clientIp)) {
            throw new RuntimeException("Access denied for IP: " + clientIp);
        }
        System.out.println("Access allowed for IP: " + clientIp);
    }

    private String getClientIP() {
        // 실제로 HttpServletRequest에서 IP를 가져오는 로직을 사용
        return "192.168.0.1"; // 예제용
    }
}
```

---

## **44. 요청별 세션 데이터 초기화 (Session Initialization)**  
HTTP 요청마다 세션 데이터를 초기화하거나 설정합니다.

**구현 예제**  
```java
@Aspect
@Component
public class SessionInitializationAspect {

    @Before("execution(* com.example.controller..*(..))")
    public void initializeSessionData() {
        System.out.println("Initializing session data...");
        // 세션 데이터 초기화 로직
    }
}
```

---

## **45. 서비스 계층 장애 감지 (Service Failure Detection)**  
특정 서비스 계층에서의 장애 발생률을 모니터링하고 알림을 전송합니다.

**구현 예제**  
```java
@Aspect
@Component
public class FailureDetectionAspect {

    private final Map<String, Integer> failureCount = new HashMap<>();
    private static final int FAILURE_THRESHOLD = 3;

    @AfterThrowing(pointcut = "execution(* com.example.service..*(..))", throwing = "ex")
    public void detectFailures(JoinPoint joinPoint, Throwable ex) {
        String methodName = joinPoint.getSignature().toString();
        failureCount.put(methodName, failureCount.getOrDefault(methodName, 0) + 1);

        if (failureCount.get(methodName) >= FAILURE_THRESHOLD) {
            System.err.println("Failure threshold exceeded for method: " + methodName);
            sendAlert(methodName);
        }
    }

    private void sendAlert(String methodName) {
        // 알림 전송 로직 (예: 이메일, Slack)
        System.out.println("Alert sent for method: " + methodName);
    }
}
```

---
여기에는 Spring AOP를 활용해 추가로 구현할 수 있는 더 많은 유용한 기능들을 소개합니다. 다양한 사례와 아이디어로 활용할 수 있습니다.

---

## **46. 데이터베이스 페일오버 처리 (Database Failover Handling)**  
주 데이터베이스 장애 발생 시 대체 데이터베이스로 자동 전환.

**구현 예제**  
```java
@Aspect
@Component
public class DatabaseFailoverAspect {

    private boolean primaryDatabaseDown = false;

    @Around("execution(* com.example.repository..*(..))")
    public Object handleFailover(ProceedingJoinPoint joinPoint) throws Throwable {
        try {
            if (!primaryDatabaseDown) {
                System.out.println("Using primary database...");
                return joinPoint.proceed();
            }
        } catch (Exception ex) {
            System.err.println("Primary database failed. Switching to backup database...");
            primaryDatabaseDown = true;
            return useBackupDatabase(joinPoint);
        }
        return useBackupDatabase(joinPoint);
    }

    private Object useBackupDatabase(ProceedingJoinPoint joinPoint) throws Throwable {
        // 여기서 backup 데이터베이스를 사용하는 로직 추가
        System.out.println("Executing with backup database");
        return joinPoint.proceed(); // 예제에서는 그냥 진행
    }
}
```

---

## **47. 사용자 활동 기록 (User Activity Logging)**  
사용자가 수행한 모든 주요 작업을 기록합니다.

**구현 예제**  
```java
@Aspect
@Component
public class UserActivityLoggingAspect {

    @AfterReturning("execution(* com.example.controller..*(..))")
    public void logUserActivity(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        String userId = getCurrentUserId();
        System.out.println("User " + userId + " performed action: " + methodName);
        saveActivityToDatabase(userId, methodName);
    }

    private String getCurrentUserId() {
        // 보안 컨텍스트에서 현재 사용자 ID 가져오기
        return "user123"; // 예제용
    }

    private void saveActivityToDatabase(String userId, String action) {
        // 데이터베이스에 사용자 활동 저장 로직
        System.out.println("Activity saved: User=" + userId + ", Action=" + action);
    }
}
```

---

## **48. API 응답 압축 (Response Compression)**  
컨트롤러의 모든 응답을 GZIP으로 압축하여 클라이언트로 전송합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ResponseCompressionAspect {

    @Around("execution(* com.example.controller..*(..))")
    public Object compressResponse(ProceedingJoinPoint joinPoint) throws Throwable {
        Object response = joinPoint.proceed();

        if (response instanceof String) {
            String compressed = compress((String) response);
            System.out.println("Response compressed");
            return compressed;
        }
        return response;
    }

    private String compress(String data) {
        // 간단한 GZIP 압축 로직
        return Base64.getEncoder().encodeToString(data.getBytes());
    }
}
```

---

## **49. 요청 프로파일링 (Request Profiling)**  
요청의 시작 시간, 끝 시간, 실행 시간 등을 기록하여 성능 분석.

**구현 예제**  
```java
@Aspect
@Component
public class RequestProfilingAspect {

    @Around("execution(* com.example.controller..*(..))")
    public Object profileRequest(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object response = joinPoint.proceed();
        long end = System.currentTimeMillis();

        System.out.println("Method " + joinPoint.getSignature() + " executed in " + (end - start) + " ms");
        return response;
    }
}
```

---

## **50. 서비스 호출 패턴 감지 (Service Call Pattern Detection)**  
특정 서비스가 지나치게 빈번히 호출되는 경우 경고.

**구현 예제**  
```java
@Aspect
@Component
public class ServiceCallPatternAspect {

    private final Map<String, Long> callTimestamps = new HashMap<>();
    private static final long THRESHOLD = 1000; // 1초 이내 반복 호출 경고

    @Before("execution(* com.example.service..*(..))")
    public void detectRapidCalls(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        long currentTime = System.currentTimeMillis();

        if (callTimestamps.containsKey(methodName)) {
            long lastCall = callTimestamps.get(methodName);
            if (currentTime - lastCall < THRESHOLD) {
                System.err.println("Warning: Method " + methodName + " is being called too frequently!");
            }
        }

        callTimestamps.put(methodName, currentTime);
    }
}
```

---

## **51. 테스트 환경 모드 처리 (Test Mode Handling)**  
테스트 환경에서는 특정 동작을 스킵하거나 대체 동작을 실행합니다.

**구현 예제**  
```java
@Aspect
@Component
public class TestModeAspect {

    private static final boolean TEST_MODE = true;

    @Around("execution(* com.example.service..*(..)) && @annotation(com.example.annotations.TestModeOnly)")
    public Object handleTestMode(ProceedingJoinPoint joinPoint) throws Throwable {
        if (TEST_MODE) {
            System.out.println("Test mode active, skipping: " + joinPoint.getSignature());
            return null; // 테스트 환경에서는 동작 생략
        }
        return joinPoint.proceed();
    }
}
```

---

## **52. 서비스 사용량 제한 (Quota Management)**  
사용자가 지정된 서비스 사용량을 초과하지 않도록 제한합니다.

**구현 예제**  
```java
@Aspect
@Component
public class QuotaManagementAspect {

    private final Map<String, Integer> userQuotas = new HashMap<>();
    private static final int MAX_QUOTA = 100;

    @Before("execution(* com.example.service..*(..)) && @annotation(com.example.annotations.QuotaLimited)")
    public void enforceQuota(JoinPoint joinPoint) {
        String userId = getCurrentUserId();
        int currentQuota = userQuotas.getOrDefault(userId, 0);

        if (currentQuota >= MAX_QUOTA) {
            throw new RuntimeException("Quota exceeded for user: " + userId);
        }

        userQuotas.put(userId, currentQuota + 1);
        System.out.println("Quota used by " + userId + ": " + (currentQuota + 1));
    }

    private String getCurrentUserId() {
        // 현재 사용자 ID 가져오기 로직
        return "user123"; // 예제용
    }
}
```

---

## **53. 요청 실행 순서 추적 (Execution Order Tracking)**  
다단계 요청 실행 흐름을 추적하여 디버깅 정보를 제공합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ExecutionOrderTrackingAspect {

    private int sequence = 0;

    @Before("execution(* com.example.service..*(..))")
    public void trackExecutionOrder(JoinPoint joinPoint) {
        sequence++;
        System.out.println("Execution order " + sequence + ": " + joinPoint.getSignature());
    }
}
```

---

## **54. 비동기 오류 처리 (Async Error Handling)**  
비동기로 실행되는 메서드에서 발생하는 예외를 중앙에서 처리합니다.

**구현 예제**  
```java
@Aspect
@Component
public class AsyncErrorHandlingAspect {

    @AfterThrowing(pointcut = "execution(* com.example.service..*(..)) && @annotation(org.springframework.scheduling.annotation.Async)", throwing = "ex")
    public void handleAsyncError(JoinPoint joinPoint, Throwable ex) {
        System.err.println("Async error in method: " + joinPoint.getSignature() + ", error: " + ex.getMessage());
        sendErrorNotification(joinPoint.getSignature().toString(), ex);
    }

    private void sendErrorNotification(String method, Throwable ex) {
        // 오류 알림 로직 (예: 이메일, Slack)
        System.out.println("Error notification sent for method: " + method);
    }
}
```

---

## **55. 비밀 유지 계약(NDA) 로깅**  
특정 메서드가 호출될 때, 실행된 동작이 NDA(Non-Disclosure Agreement)에 따라 로그에 포함되지 않도록 처리.

**구현 예제**  
```java
@Aspect
@Component
public class NDALoggingAspect {

    @Around("@annotation(com.example.annotations.NDAProtected)")
    public Object handleNDALogging(ProceedingJoinPoint joinPoint) throws Throwable {
        try {
            System.out.println("NDA-protected method called: " + joinPoint.getSignature());
            return joinPoint.proceed();
        } finally {
            System.out.println("Execution of NDA-protected method completed. No details logged.");
        }
    }
}
```

---

## **56. 컨트롤러 입력값 스니핑 방지 (Input Sniffing Prevention)**  
사용자의 입력값에 악성 코드가 포함되어 있는지 탐지하고 차단합니다.

**구현 예제**  
```java
@Aspect
@Component
public class InputValidationAspect {

    @Before("execution(* com.example.controller..*(..))")
    public void validateInput(JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs();
        for (Object arg : args) {
            if (arg instanceof String && containsMaliciousCode((String) arg)) {
                throw new IllegalArgumentException("Malicious input detected: " + arg);
            }
        }
    }

    private boolean containsMaliciousCode(String input) {
        // 간단한 악성 코드 탐지 로직
        return input.contains("<script>") || input.contains("DROP TABLE");
    }
}
```

---

## **57. 애플리케이션 상태 체크 (Application Health Monitoring)**  
특정 메서드가 호출될 때 애플리케이션의 상태를 체크하고 필요시 알림을 전송.

**구현 예제**  
```java
@Aspect
@Component
public class ApplicationHealthAspect {

    @Before("execution(* com.example.service..*(..)) && @annotation(com.example.annotations.HealthCheck)")
    public void checkApplicationHealth() {
        if (!isApplicationHealthy()) {
            System.err.println("Application health check failed!");
            sendHealthAlert();
        } else {
            System.out.println("Application is healthy.");
        }
    }

    private boolean isApplicationHealthy() {
        // 간단한 상태 체크 로직 (예: 메모리 사용량, 디스크 상태 등)
        return true; // 예제용
    }

    private void sendHealthAlert() {
        // 건강 상태 알림 전송 로직
        System.out.println("Health alert sent to monitoring system.");
    }
}
```

---

## **58. 데이터 변경 감사 로그 작성 (Audit Logging with Details)**  
데이터베이스에서 데이터가 변경되었을 때 변경 전후의 값을 감사 로그로 작성.

**구현 예제**  
```java
@Aspect
@Component
public class AuditDetailAspect {

    @Around("@annotation(com.example.annotations.AuditChanges)")
    public Object logChanges(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Capturing audit log for method: " + joinPoint.getSignature());
        Object[] args = joinPoint.getArgs();

        // 변경 전 데이터 가져오기
        Object beforeChange = fetchCurrentData(args);

        Object result = joinPoint.proceed();

        // 변경 후 데이터 가져오기
        Object afterChange = fetchCurrentData(args);

        // 감사 로그 작성
        logAuditDetails(beforeChange, afterChange);

        return result;
    }

    private Object fetchCurrentData(Object[] args) {
        // 현재 데이터를 가져오는 로직 (예: ID로 조회)
        return "Sample Data"; // 예제용
    }

    private void logAuditDetails(Object before, Object after) {
        System.out.println("Audit Log -> Before: " + before + ", After: " + after);
    }
}
```

---

## **59. 외부 API 호출 자동 재시도 (External API Retry Mechanism)**  
외부 API 호출이 실패할 경우 일정 횟수까지 재시도합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ExternalAPIRetryAspect {

    @Around("@annotation(com.example.annotations.RetryOnFailure)")
    public Object retryAPIRequest(ProceedingJoinPoint joinPoint) throws Throwable {
        int maxRetries = 3;
        int attempts = 0;

        while (true) {
            try {
                return joinPoint.proceed();
            } catch (Exception ex) {
                attempts++;
                System.err.println("API call failed. Attempt " + attempts);
                if (attempts >= maxRetries) {
                    throw ex;
                }
            }
        }
    }
}
```

---

## **60. 비밀번호 유효성 검사 (Password Strength Validation)**  
사용자가 입력한 비밀번호가 규칙에 맞는지 검증.

**구현 예제**  
```java
@Aspect
@Component
public class PasswordValidationAspect {

    @Before("@annotation(com.example.annotations.ValidatePassword)")
    public void validatePassword(JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs();
        for (Object arg : args) {
            if (arg instanceof String && !isValidPassword((String) arg)) {
                throw new IllegalArgumentException("Invalid password: " + arg);
            }
        }
    }

    private boolean isValidPassword(String password) {
        // 비밀번호 강도 검사 (예: 최소 길이, 특수 문자 포함 여부 등)
        return password.length() >= 8 && password.matches(".*[!@#$%^&*()].*");
    }
}
```

---

## **61. 지연 초기화 (Lazy Initialization)**  
특정 메서드의 결과를 최초 호출 시 초기화하고 캐싱하여 재사용.

**구현 예제**  
```java
@Aspect
@Component
public class LazyInitializationAspect {

    private final Map<String, Object> cache = new HashMap<>();

    @Around("@annotation(com.example.annotations.LazyInit)")
    public Object handleLazyInit(ProceedingJoinPoint joinPoint) throws Throwable {
        String key = joinPoint.getSignature().toString();

        if (cache.containsKey(key)) {
            System.out.println("Returning cached result for: " + key);
            return cache.get(key);
        }

        Object result = joinPoint.proceed();
        cache.put(key, result);
        System.out.println("Result cached for: " + key);
        return result;
    }
}
```

---

## **62. 사용자 시간대 기반 데이터 처리 (Time Zone Based Processing)**  
사용자의 시간대에 맞춰 데이터를 처리.

**구현 예제**  
```java
@Aspect
@Component
public class TimeZoneProcessingAspect {

    @Around("@annotation(com.example.annotations.TimeZoneAware)")
    public Object adjustForTimeZone(ProceedingJoinPoint joinPoint) throws Throwable {
        String userTimeZone = getUserTimeZone();
        System.out.println("Adjusting data for user time zone: " + userTimeZone);

        // 시간대 조정 로직
        Object result = joinPoint.proceed();
        return adjustResultForTimeZone(result, userTimeZone);
    }

    private String getUserTimeZone() {
        // 사용자의 시간대 가져오는 로직 (예: 요청 헤더에서 추출)
        return "Asia/Seoul"; // 예제용
    }

    private Object adjustResultForTimeZone(Object result, String timeZone) {
        // 시간대에 맞게 데이터를 조정하는 로직
        return result; // 예제용
    }
}
```

---

## **63. API 요청별 실행 우선순위 처리 (Priority-Based Execution)**  
API 요청에 우선순위를 부여하여 중요한 요청을 먼저 처리.

**구현 예제**  
```java
@Aspect
@Component
public class PriorityExecutionAspect {

    @Around("@annotation(com.example.annotations.Priority)")
    public Object prioritizeRequest(ProceedingJoinPoint joinPoint) throws Throwable {
        String priority = getPriorityFromRequest();
        System.out.println("Handling request with priority: " + priority);

        // 우선순위에 따라 처리 로직 추가
        return joinPoint.proceed();
    }

    private String getPriorityFromRequest() {
        // 요청에서 우선순위를 추출 (예: 요청 헤더 또는 파라미터)
        return "HIGH"; // 예제용
    }
}
```

---

## **64. 요청 응답 시간 로깅 (Request-Response Time Logging)**  
요청 처리의 전체 시간을 측정하고 로깅.

**구현 예제**  
```java
@Aspect
@Component
public class RequestResponseTimeAspect {

    @Around("execution(* com.example.controller..*(..))")
    public Object logRequestResponseTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long end = System.currentTimeMillis();

        System.out.println("Request to " + joinPoint.getSignature() + " completed in " + (end - start) + " ms");
        return result;
    }
}
```

---

## **65. API 요청 크기 제한 (Request Size Limiting)**  
API 요청의 데이터 크기를 제한하여 과도한 데이터 전송 방지.

**구현 예제**  
```java
@Aspect
@Component
public class RequestSizeLimitingAspect {

    private static final int MAX_SIZE = 1024 * 1024; // 1MB

    @Before("execution(* com.example.controller..*(..))")
    public void limitRequestSize(JoinPoint joinPoint) {
        for (Object arg : joinPoint.getArgs()) {
            if (arg instanceof String && ((String) arg).length() > MAX_SIZE) {
                throw new IllegalArgumentException("Request size exceeds the allowed limit.");
            }
        }
    }
}
```

---

## **66. 요청 리플레이 방지 (Request Replay Protection)**  
특정 요청이 중복해서 처리되지 않도록 방지.

**구현 예제**  
```java
@Aspect
@Component
public class ReplayProtectionAspect {

    private final Set<String> processedRequests = Collections.synchronizedSet(new HashSet<>());

    @Before("@annotation(com.example.annotations.ReplayProtected)")
    public void preventReplay(JoinPoint joinPoint) {
        String requestId = extractRequestId();
        if (processedRequests.contains(requestId)) {
            throw new IllegalStateException("Duplicate request detected: " + requestId);
        }
        processedRequests.add(requestId);
    }

    private String extractRequestId() {
        // 요청 ID 추출 로직 (예: 헤더에서 가져오기)
        return UUID.randomUUID().toString(); // 예제용
    }
}
```

---

## **67. 사용자별 데이터 처리 속도 제한 (Rate Limit per User)**  
사용자별 데이터 처리 속도를 제한.

**구현 예제**  
```java
@Aspect
@Component
public class UserRateLimitAspect {

    private final Map<String, Long> userLastRequestTime = new ConcurrentHashMap<>();
    private static final long MIN_INTERVAL = 2000; // 2초 간격

    @Before("execution(* com.example.controller..*(..))")
    public void enforceUserRateLimit() {
        String userId = getCurrentUserId();
        long now = System.currentTimeMillis();

        if (userLastRequestTime.containsKey(userId)) {
            long lastRequestTime = userLastRequestTime.get(userId);
            if (now - lastRequestTime < MIN_INTERVAL) {
                throw new RuntimeException("User " + userId + " is sending requests too quickly.");
            }
        }

        userLastRequestTime.put(userId, now);
    }

    private String getCurrentUserId() {
        // 사용자 ID 가져오기 로직
        return "user123"; // 예제용
    }
}
```

---

## **68. 메서드 호출 통계 (Method Invocation Statistics)**  
특정 메서드가 얼마나 자주 호출되는지 기록하고 분석.

**구현 예제**  
```java
@Aspect
@Component
public class MethodInvocationStatisticsAspect {

    private final Map<String, Integer> methodCallCounts = new ConcurrentHashMap<>();

    @After("execution(* com.example.service..*(..))")
    public void trackMethodCalls(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        methodCallCounts.put(methodName, methodCallCounts.getOrDefault(methodName, 0) + 1);
        System.out.println("Method " + methodName + " has been called " + methodCallCounts.get(methodName) + " times.");
    }
}
```

---

## **69. 특정 필드 제거 후 로깅 (Exclude Sensitive Fields)**  
로그 출력 시 민감한 데이터를 제거합니다.

**구현 예제**  
```java
@Aspect
@Component
public class SensitiveFieldRemovalAspect {

    @Around("execution(* com.example.service..*(..))")
    public Object removeSensitiveFieldsFromLog(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = joinPoint.proceed();

        if (result instanceof Map) {
            Map<String, Object> data = (Map<String, Object>) result;
            data.remove("password");
            data.remove("creditCardNumber");
        }

        return result;
    }
}
```

---

## **70. API 사용량 모니터링 (API Usage Monitoring)**  
API 호출 사용량을 추적하여 과도한 요청에 대한 경고를 제공합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ApiUsageMonitoringAspect {

    private final Map<String, Integer> apiUsageCounts = new ConcurrentHashMap<>();
    private static final int MAX_USAGE_LIMIT = 100;

    @After("execution(* com.example.controller..*(..))")
    public void monitorApiUsage(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().toShortString();
        apiUsageCounts.put(methodName, apiUsageCounts.getOrDefault(methodName, 0) + 1);

        if (apiUsageCounts.get(methodName) > MAX_USAGE_LIMIT) {
            System.err.println("Warning: API usage limit exceeded for " + methodName);
        }
    }
}
```

---

## **71. 요청 응답 디버깅 (Request-Response Debugging)**  
요청 및 응답 데이터를 캡처하고 디버깅 로그를 출력.

**구현 예제**  
```java
@Aspect
@Component
public class RequestResponseDebuggingAspect {

    @Around("execution(* com.example.controller..*(..))")
    public Object logRequestAndResponse(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Request to: " + joinPoint.getSignature());
        System.out.println("Arguments: " + Arrays.toString(joinPoint.getArgs()));

        Object response = joinPoint.proceed();

        System.out.println("Response from: " + joinPoint.getSignature());
        System.out.println("Response Data: " + response);
        return response;
    }
}
```

---

## **72. 오래 실행되는 요청 탐지 (Long-Running Request Detection)**  
특정 시간 이상 실행되는 요청을 탐지하여 경고.

**구현 예제**  
```java
@Aspect
@Component
public class LongRunningRequestAspect {

    private static final long WARNING_THRESHOLD = 3000; // 3초

    @Around("execution(* com.example.service..*(..))")
    public Object detectLongRunningRequests(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;

        if (duration > WARNING_THRESHOLD) {
            System.err.println("Warning: Long-running request detected in " + joinPoint.getSignature() + " (Duration: " + duration + " ms)");
        }

        return result;
    }
}
```

---

## **73. 메서드 실행 제한 시간 초과 경고 (Timeout Warning)**  
특정 메서드가 지정된 시간 내에 완료되지 않으면 경고를 출력.

**구현 예제**  
```java
@Aspect
@Component
public class MethodTimeoutWarningAspect {

    private static final long TIMEOUT_THRESHOLD = 2000; // 2초

    @Around("execution(* com.example.service..*(..))")
    public Object monitorMethodTimeout(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;

        if (duration > TIMEOUT_THRESHOLD) {
            System.err.println("Warning: Method " + joinPoint.getSignature() + " took too long (" + duration + " ms)");
        }

        return result;
    }
}
```

---

## **74. 데이터 사본 생성 및 복원 (Backup and Restore Data)**  
데이터 변경 작업 전에 사본을 생성하고, 실패 시 복원.

**구현 예제**  
```java
@Aspect
@Component
public class DataBackupAspect {

    private final Map<String, Object> backupData = new ConcurrentHashMap<>();

    @Around("@annotation(com.example.annotations.BackupRestore)")
    public Object handleBackupAndRestore(ProceedingJoinPoint joinPoint) throws Throwable {
        String key = joinPoint.getSignature().toString();

        try {
            backupData.put(key, createBackup());
            return joinPoint.proceed();
        } catch (Exception ex) {
            restoreBackup(key);
            throw ex;
        }
    }

    private Object createBackup() {
        // 데이터 백업 로직
        System.out.println("Backup created");
        return "BackupData"; // 예제용
    }

    private void restoreBackup(String key) {
        // 데이터 복원 로직
        System.out.println("Restoring backup for key: " + key);
    }
}
```

---

## **75. HTTP 요청의 헤더 검증 (Request Header Validation)**  
HTTP 요청 헤더에 필수 정보가 포함되어 있는지 검증.

**구현 예제**  
```java
@Aspect
@Component
public class RequestHeaderValidationAspect {

    @Before("execution(* com.example.controller..*(..))")
    public void validateHeaders() {
        String requiredHeader = getHeader("X-Required-Header");
        if (requiredHeader == null || requiredHeader.isEmpty()) {
            throw new IllegalArgumentException("Missing required header: X-Required-Header");
        }
    }

    private String getHeader(String headerName) {
        // 요청 헤더 가져오기 (HttpServletRequest에서)
        return "ValidHeader"; // 예제용
    }
}
```

---

## **76. 데이터 일관성 확인 (Data Consistency Check)**  
메서드 호출 후 데이터베이스의 상태를 확인하여 데이터 일관성을 유지.

**구현 예제**  
```java
@Aspect
@Component
public class DataConsistencyAspect {

    @After("execution(* com.example.repository..*(..))")
    public void checkDataConsistency() {
        if (!isDataConsistent()) {
            System.err.println("Data inconsistency detected!");
            handleInconsistency();
        }
    }

    private boolean isDataConsistent() {
        // 데이터 일관성 확인 로직
        return true; // 예제용
    }

    private void handleInconsistency() {
        // 데이터 불일치 처리 로직
        System.out.println("Handling data inconsistency...");
    }
}
```

---

## **77. 동적 기능 활성화 (Dynamic Feature Toggle)**  
외부 설정값에 따라 메서드 실행 여부를 동적으로 제어.

**구현 예제**  
```java
@Aspect
@Component
public class FeatureToggleAspect {

    @Around("@annotation(com.example.annotations.FeatureToggle)")
    public Object handleFeatureToggle(ProceedingJoinPoint joinPoint) throws Throwable {
        String featureName = getFeatureName(joinPoint);
        if (isFeatureEnabled(featureName)) {
            System.out.println("Feature " + featureName + " is enabled");
            return joinPoint.proceed();
        } else {
            System.out.println("Feature " + featureName + " is disabled");
            return null;
        }
    }

    private String getFeatureName(ProceedingJoinPoint joinPoint) {
        // 어노테이션에서 기능 이름 추출
        return "NewFeature"; // 예제용
    }

    private boolean isFeatureEnabled(String featureName) {
        // 외부 설정값으로 기능 활성화 여부 결정
        return true; // 예제용
    }
}
```

---

## **78. API 응답 캐시 무효화 (Invalidate Cache on Response)**  
특정 조건에서 API 응답 캐시를 무효화.

**구현 예제**  
```java
@Aspect
@Component
public class CacheInvalidationAspect {

    @After("@annotation(com.example.annotations.InvalidateCache)")
    public void invalidateCache() {
        System.out.println("Invalidating cache for the current operation...");
        // 캐시 무효화 로직
    }
}
```

---

## **79. 메서드 호출 흐름 추적 (Call Flow Tracing)**  
메서드 호출 흐름을 추적하여 디버깅.

**구현 예제**  
```java
@Aspect
@Component
public class CallFlowTracingAspect {

    private final ThreadLocal<Stack<String>> callStack = ThreadLocal.withInitial(Stack::new);

    @Before("execution(* com.example..*(..))")
    public void beforeMethod(JoinPoint joinPoint) {
        callStack.get().push(joinPoint.getSignature().toShortString());
        System.out.println("Entering: " + joinPoint.getSignature());
    }

    @After("execution(* com.example..*(..))")
    public void afterMethod(JoinPoint joinPoint) {
        System.out.println("Exiting: " + callStack.get().pop());
    }
}
```

---

## **80. 트랜잭션 롤백 후 처리 (Post Rollback Handling)**  
트랜잭션이 롤백된 후 추가 작업을 수행.

**구현 예제**  
```java
@Aspect
@Component
public class RollbackHandlingAspect {

    @AfterThrowing(pointcut = "execution(* com.example.service..*(..)) && @annotation(org.springframework.transaction.annotation.Transactional)", throwing = "ex")
    public void handleRollback(Throwable ex) {
        System.err.println("Transaction rolled back due to: " + ex.getMessage());
        // 롤백 후 작업 (예: 알림 전송, 복구 작업)
    }
}
```

---

## **81. 사용자 활동의 세부 로그 생성 (Detailed User Activity Logging)**  
사용자가 수행한 작업의 세부 로그를 생성하여 분석.

**구현 예제**  
```java
@Aspect
@Component
public class DetailedUserActivityAspect {

    @After("execution(* com.example.controller..*(..))")
    public void logDetailedUserActivity(JoinPoint joinPoint) {
        String userId = getCurrentUserId();
        String methodName = joinPoint.getSignature().toShortString();
        System.out.println("User " + userId + " accessed " + methodName);
        saveDetailedActivityLog(userId, methodName);
    }

    private void saveDetailedActivityLog(String userId, String action) {
        // 사용자 활동 로그 저장 로직
        System.out.println("Activity saved: User=" + userId + ", Action=" + action);
    }

    private String getCurrentUserId() {
        return "user123"; // 예제용
    }
}
```

---

## **82. 글로벌 메서드 실행 모니터링 (Global Method Execution Monitoring)**  
애플리케이션 내에서 모든 메서드 실행을 모니터링하여 통계 생성.

**구현 예제**  
```java
@Aspect
@Component
public class GlobalMethodMonitoringAspect {

    private final Map<String, Long> executionCounts = new ConcurrentHashMap<>();
    private final Map<String, Long> executionDurations = new ConcurrentHashMap<>();

    @Around("execution(* com.example..*(..))")
    public Object monitorMethodExecution(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().toShortString();
        long start = System.currentTimeMillis();

        Object result = joinPoint.proceed();

        long duration = System.currentTimeMillis() - start;
        executionCounts.put(methodName, executionCounts.getOrDefault(methodName, 0L) + 1);
        executionDurations.put(methodName, executionDurations.getOrDefault(methodName, 0L) + duration);

        System.out.println("Executed " + methodName + " in " + duration + " ms");
        return result;
    }

    public void printStatistics() {
        executionCounts.forEach((method, count) -> {
            long totalDuration = executionDurations.get(method);
            System.out.println("Method: " + method + ", Count: " + count + ", Avg Time: " + (totalDuration / count) + " ms");
        });
    }
}
```

---

## **83. 비동기 메서드 병렬 실행 제한 (Async Method Parallel Execution Limit)**  
비동기로 실행되는 메서드의 병렬 실행 개수를 제한.

**구현 예제**  
```java
@Aspect
@Component
public class AsyncParallelExecutionLimitAspect {

    private final Semaphore semaphore = new Semaphore(5); // 최대 병렬 실행 개수 제한

    @Around("@annotation(org.springframework.scheduling.annotation.Async)")
    public Object limitAsyncExecution(ProceedingJoinPoint joinPoint) throws Throwable {
        if (!semaphore.tryAcquire()) {
            throw new RuntimeException("Too many parallel executions. Try again later.");
        }
        try {
            return joinPoint.proceed();
        } finally {
            semaphore.release();
        }
    }
}
```

---

## **84. 동적 서비스 변경 (Dynamic Service Switching)**  
특정 조건에 따라 서비스 인스턴스를 동적으로 변경.

**구현 예제**  
```java
@Aspect
@Component
public class DynamicServiceSwitchingAspect {

    @Around("execution(* com.example.service..*(..))")
    public Object switchService(ProceedingJoinPoint joinPoint) throws Throwable {
        if (shouldUseAlternativeService()) {
            System.out.println("Using alternative service for: " + joinPoint.getSignature());
            return useAlternativeService(joinPoint);
        }
        return joinPoint.proceed();
    }

    private boolean shouldUseAlternativeService() {
        // 서비스 변경 조건
        return Math.random() > 0.5; // 예제용
    }

    private Object useAlternativeService(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Alternative service logic executed.");
        // 실제로 대체 서비스 호출 로직 작성
        return null; // 예제용
    }
}
```

---

## **85. 데이터 조회 실패 대체 데이터 제공 (Fallback Data Provider)**  
데이터 조회 실패 시 기본값 또는 캐시 데이터를 제공.

**구현 예제**  
```java
@Aspect
@Component
public class FallbackDataAspect {

    @Around("execution(* com.example.repository..*(..))")
    public Object provideFallbackData(ProceedingJoinPoint joinPoint) throws Throwable {
        try {
            return joinPoint.proceed();
        } catch (Exception ex) {
            System.err.println("Failed to fetch data. Providing fallback.");
            return getFallbackData(joinPoint);
        }
    }

    private Object getFallbackData(ProceedingJoinPoint joinPoint) {
        // 대체 데이터 제공 로직
        return "FallbackData"; // 예제용
    }
}
```

---

## **86. 사용자 지정 요청 추적 ID 생성 (Custom Request Trace ID)**  
각 요청에 고유한 추적 ID를 생성하여 로깅과 디버깅에 활용.

**구현 예제**  
```java
@Aspect
@Component
public class RequestTraceIdAspect {

    private final ThreadLocal<String> traceId = new ThreadLocal<>();

    @Before("execution(* com.example.controller..*(..))")
    public void generateTraceId() {
        traceId.set(UUID.randomUUID().toString());
        System.out.println("Generated Trace ID: " + traceId.get());
    }

    @After("execution(* com.example.controller..*(..))")
    public void clearTraceId() {
        System.out.println("Clearing Trace ID: " + traceId.get());
        traceId.remove();
    }

    public String getTraceId() {
        return traceId.get();
    }
}
```

---

## **87. 사용자 세션 기반 접근 제어 (Session-Based Access Control)**  
사용자 세션 상태에 따라 특정 API 접근을 제한.

**구현 예제**  
```java
@Aspect
@Component
public class SessionAccessControlAspect {

    @Before("@annotation(com.example.annotations.SessionRestricted)")
    public void restrictAccessBasedOnSession() {
        if (!isSessionActive()) {
            throw new IllegalStateException("User session is not active.");
        }
    }

    private boolean isSessionActive() {
        // 세션 상태 확인 로직
        return true; // 예제용
    }
}
```

---

## **88. 캐시 업데이트 시 알림 전송 (Notify on Cache Update)**  
캐시가 업데이트될 때 관리자나 모니터링 시스템에 알림을 전송.

**구현 예제**  
```java
@Aspect
@Component
public class CacheUpdateNotificationAspect {

    @After("@annotation(org.springframework.cache.annotation.CachePut)")
    public void notifyCacheUpdate() {
        System.out.println("Cache updated. Sending notification...");
        sendCacheUpdateNotification();
    }

    private void sendCacheUpdateNotification() {
        // 알림 전송 로직 (예: 이메일, 슬랙)
        System.out.println("Notification sent.");
    }
}
```

---

## **89. 사용자별 트랜잭션 추적 (User-Specific Transaction Tracking)**  
각 사용자별로 트랜잭션 실행 내역을 추적.

**구현 예제**  
```java
@Aspect
@Component
public class UserTransactionTrackingAspect {

    @AfterReturning("@annotation(org.springframework.transaction.annotation.Transactional)")
    public void trackTransaction(JoinPoint joinPoint) {
        String userId = getCurrentUserId();
        String methodName = joinPoint.getSignature().toShortString();
        System.out.println("Transaction completed by user: " + userId + " on method: " + methodName);
        saveTransactionLog(userId, methodName);
    }

    private String getCurrentUserId() {
        // 사용자 ID 가져오기 로직
        return "user123"; // 예제용
    }

    private void saveTransactionLog(String userId, String methodName) {
        // 트랜잭션 로그 저장
        System.out.println("Transaction log saved for user: " + userId + ", method: " + methodName);
    }
}
```

---

## **90. 커스텀 메서드 리턴값 변환 (Custom Return Value Transformation)**  
특정 메서드의 반환값을 동적으로 변환.

**구현 예제**  
```java
@Aspect
@Component
public class ReturnValueTransformationAspect {

    @AfterReturning(pointcut = "execution(* com.example.service..*(..))", returning = "result")
    public Object transformReturnValue(JoinPoint joinPoint, Object result) {
        if (result instanceof String) {
            return ((String) result).toUpperCase();
        }
        return result;
    }
}
```

---

## **91. 조건부 로깅 (Conditional Logging)**  
특정 조건을 만족할 때만 메서드 실행을 로깅합니다.

**구현 예제**  
```java
@Aspect
@Component
public class ConditionalLoggingAspect {

    @Around("execution(* com.example.service..*(..)) && @annotation(com.example.annotations.ConditionalLog)")
    public Object logConditionally(ProceedingJoinPoint joinPoint) throws Throwable {
        if (shouldLog(joinPoint)) {
            System.out.println("Executing method: " + joinPoint.getSignature());
        }
        return joinPoint.proceed();
    }

    private boolean shouldLog(ProceedingJoinPoint joinPoint) {
        // 조건 정의 (예: 특정 파라미터 값, 현재 환경 등)
        return true; // 예제에서는 항상 로깅
    }
}
```

---

## **92. 데이터 입력 이력 관리 (Data Input History Tracking)**  
모든 데이터 입력 내역을 저장하여 추적 가능하도록 만듭니다.

**구현 예제**  
```java
@Aspect
@Component
public class DataInputHistoryAspect {

    @After("execution(* com.example.service..*(..))")
    public void trackInputHistory(JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs();
        for (Object arg : args) {
            saveInputHistory(arg);
        }
    }

    private void saveInputHistory(Object input) {
        // 데이터 입력 이력 저장 로직
        System.out.println("Input history saved: " + input);
    }
}
```

---

## **93. 메서드 호출 순서 보장 (Ensure Method Invocation Order)**  
특정 메서드 호출 순서를 보장하여 의도한 흐름을 유지합니다.

**구현 예제**  
```java
@Aspect
@Component
public class MethodInvocationOrderAspect {

    private final Queue<String> expectedOrder = new LinkedList<>(List.of(
        "firstMethod", "secondMethod", "thirdMethod"
    ));

    @Before("execution(* com.example.service..*(..))")
    public void ensureOrder(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        if (!expectedOrder.isEmpty() && !expectedOrder.peek().equals(methodName)) {
            throw new IllegalStateException("Method " + methodName + " called out of order.");
        }
        expectedOrder.poll();
    }
}
```

---

## **94. 특정 파라미터 기반 접근 제어 (Parameter-Based Access Control)**  
메서드 파라미터 값에 따라 실행 여부를 제어.

**구현 예제**  
```java
@Aspect
@Component
public class ParameterBasedAccessControlAspect {

    @Before("execution(* com.example.service..*(..)) && args(param,..)")
    public void restrictAccess(Object param) {
        if (!hasAccess(param)) {
            throw new SecurityException("Access denied for parameter: " + param);
        }
    }

    private boolean hasAccess(Object param) {
        // 접근 권한 확인 로직 (예: 특정 값 허용 여부)
        return !"restricted".equals(param);
    }
}
```

---

## **95. 요청 데이터 변환 (Request Data Transformation)**  
요청 데이터를 변환하여 메서드가 처리하기 쉽게 조정.

**구현 예제**  
```java
@Aspect
@Component
public class RequestDataTransformationAspect {

    @Around("execution(* com.example.controller..*(..))")
    public Object transformRequestData(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        for (int i = 0; i < args.length; i++) {
            if (args[i] instanceof String) {
                args[i] = preprocessData((String) args[i]);
            }
        }
        return joinPoint.proceed(args);
    }

    private String preprocessData(String data) {
        // 데이터 전처리 로직 (예: 대문자 변환)
        return data.trim().toUpperCase();
    }
}
```

---

## **96. 트랜잭션 내 특정 작업 감시 (Monitor Specific Actions in Transactions)**  
트랜잭션 내부에서 특정 작업이 발생하는지 모니터링.

**구현 예제**  
```java
@Aspect
@Component
public class TransactionMonitoringAspect {

    @Around("@annotation(org.springframework.transaction.annotation.Transactional)")
    public Object monitorTransaction(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Transaction started: " + joinPoint.getSignature());
        try {
            return joinPoint.proceed();
        } finally {
            System.out.println("Transaction completed: " + joinPoint.getSignature());
        }
    }
}
```

---

## **97. 동적 메서드 실행 제한 (Dynamic Execution Blocking)**  
환경이나 조건에 따라 메서드 실행을 차단.

**구현 예제**  
```java
@Aspect
@Component
public class DynamicExecutionBlockingAspect {

    @Before("execution(* com.example.service..*(..)) && @annotation(com.example.annotations.DynamicBlock)")
    public void blockExecution(JoinPoint joinPoint) {
        if (shouldBlockExecution()) {
            throw new IllegalStateException("Method execution blocked: " + joinPoint.getSignature());
        }
    }

    private boolean shouldBlockExecution() {
        // 차단 조건 (예: 특정 환경, 설정값 등)
        return false; // 예제에서는 차단하지 않음
    }
}
```

---

## **98. HTTP 응답 데이터 필터링 (Response Data Filtering)**  
API 응답에서 민감한 정보를 필터링.

**구현 예제**  
```java
@Aspect
@Component
public class ResponseDataFilteringAspect {

    @Around("execution(* com.example.controller..*(..))")
    public Object filterResponseData(ProceedingJoinPoint joinPoint) throws Throwable {
        Object response = joinPoint.proceed();

        if (response instanceof Map) {
            Map<String, Object> data = (Map<String, Object>) response;
            data.remove("password");
            data.remove("ssn"); // 민감 데이터 제거
        }

        return response;
    }
}
```

---

## **99. 대규모 데이터 처리 모니터링 (Large Data Processing Monitoring)**  
대규모 데이터 처리 시 성능을 추적하고 경고.

**구현 예제**  
```java
@Aspect
@Component
public class LargeDataProcessingMonitoringAspect {

    private static final int LARGE_DATA_THRESHOLD = 1000;

    @Around("execution(* com.example.service..*(..))")
    public Object monitorLargeDataProcessing(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();

        for (Object arg : args) {
            if (arg instanceof List && ((List<?>) arg).size() > LARGE_DATA_THRESHOLD) {
                System.err.println("Warning: Large data processing detected in method: " + joinPoint.getSignature());
            }
        }

        return joinPoint.proceed();
    }
}
```

---

## **100. 요청 ID 전파 (Request ID Propagation)**  
요청 ID를 메서드 호출 체인 전반에 전파하여 추적 가능.

**구현 예제**  
```java
@Aspect
@Component
public class RequestIdPropagationAspect {

    private static final ThreadLocal<String> requestId = ThreadLocal.withInitial(() -> UUID.randomUUID().toString());

    @Before("execution(* com.example.controller..*(..))")
    public void propagateRequestId() {
        System.out.println("Propagating Request ID: " + requestId.get());
    }

    public static String getRequestId() {
        return requestId.get();
    }
}
```

---