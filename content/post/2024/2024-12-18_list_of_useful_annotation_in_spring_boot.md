---
title: "Spring Boot에서 자주 사용되는 애노테이션"
date: 2024-12-18T10:04:00+09:00
draft: true
categories: ["Spring"]
tags: ["annotation", "spring"]
---

이 문서는 Spring Boot 애플리케이션에서 자주 사용되는 애노테이션의 목록입니다.
<!--more-->
자세하고 포괄적인 정보는 공식 Javadocs 및 문서를 참조하십시오.

## 핵심 스프링

- [@Bean][bean] - 애노테이션이 붙은 메서드는 Spring IoC 컨테이너에 의해 관리되는 빈을 생성합니다.
- [@Primary][primary] - 후보가 여러 개인 경우 Bean에 우선권을 부여해야 함을 나타냅니다. 단일 값 종속성을 autowire할 수 있습니다. 
- 스테레오타입 애노테이션
    - [@Component][component] - 애노테이션이 붙은 클래스를 컴포넌트 스캐닝에 의해 발견되고 애플리케이션 컨텍스트에 로드되는 빈으로 표시합니다.
    - [@Controller][controller] - 애노테이션이 붙은 클래스를 Spring MVC의 요청 핸들러를 포함하는 빈으로 표시합니다.
    - [@RestController][rest-controller] - 애노테이션이 붙은 클래스를 `@Controller` 빈으로 표시하고 반환된 결과를 메시지로 직렬화하기 위해 `@ResponseBody`를 추가합니다.
    - [@Configuration][config] - 애노테이션이 붙은 클래스를 자바 설정으로 표시하여 빈을 정의합니다.
    - [@Service][service] - 애노테이션이 붙은 클래스를 빈으로 표시합니다(관례상 비즈니스 로직을 포함하는 경우가 많습니다).
    - [@Repository][repo] - 애노테이션이 붙은 클래스를 빈으로 표시하고(관례상 데이터 접근을 제공하는 경우가 많습니다) `SQLException`을 `DataAccessExceptions`로 자동 변환합니다.

### 빈 상태
- [@PostConstruct][postconstruct] - 의존성 주입이 완료된 후 초기화를 수행하기 위해 애노테이션이 붙은 메서드를 실행합니다.
- [@PreDestroy][predestroy] - 빈이 파괴되기 전에 애노테이션이 붙은 메서드를 실행합니다(예: 종료 시).

### 설정
- [@Import][import] - 하나 이상의 자바 설정 클래스 `@Configuration`를 가져옵니다.
- [@PropertySource][propertysource] - `application.properties` 파일의 위치를 지정하여 키-값 쌍을 Spring `Environment`에 추가합니다.
- [@Value][value] - 애노테이션이 붙은 필드와 매개변수 값이 주입됩니다.
- [@ComponentScan][componentscan] - 컴포넌트 스캐닝을 구성합니다(`@Component`, `@Service` 등).

### 빈 속성
- [@Lazy][lazy] - 애노테이션이 붙은 빈은 첫 사용 시 지연 초기화됩니다.
- [@Profile][profile] - 정의된 프로필이 활성화된 경우에만 빈이 초기화됩니다.
- [@Scope][scope] - 빈 생성 범위를 정의합니다(예: 프로토타입, 싱글톤 등).
- [@DependsOn][dependson] - 생성 순서 측면에서 다른 빈에 대한 종속성을 명시적으로 정의합니다.
- [@Order][order] - 빈 목록을 주입할 때 정렬 순서를 정의하지만 단일 빈이 예상되는 경우 우선순위를 해결하지는 않습니다.
- [@Primary][primary] - 여러 빈을 자동 주입할 수 있는 경우 애노테이션이 붙은 빈이 선택됩니다.
- [@Conditional][conditional] - 조건이 만족되는 경우에만 애노테이션이 붙은 빈이 생성됩니다.
    - Spring Boot에서 추가로 사용 가능:
        - [@ConditionalOnBean][conditionalonbean]
        - [@ConditionalOnMissingBean][conditionalonmissingbean]
        - [@ConditionalOnClass][conditionalonclass]
        - [@ConditionalOnMissingClass][conditionalonmissingclass]
        - [@ConditionalOnProperty][conditionalonproperty]
        - [@ConditionalOnMissingProperty][conditionalonmissingproperty]

### 빈 주입
- [@Autowired][autowired] - 빈이 애노테이션이 붙은 세터, 필드 또는 생성자 매개변수에 주입됩니다.
- [@Qualifier][qualifier] - 자동 주입 후보를 식별하기 위한 추가 조건으로 빈의 이름을 지정합니다.

### 유효성 검사
- [@Valid][valid] - 속성, 메서드 매개변수 또는 반환 유형을 유효성 검사 대상으로 표시합니다.
- [@Validated][validated] - 여러 그룹의 유효성 검사를 허용하는 `@Valid`의 변형입니다(예: 애노테이션이 붙은 클래스의 모든 필드).
- [@NotNull][notnull] - null이 아니어야 합니다.
- [@NotEmpty][notempty] - null이 아니고 비어 있지 않아야 합니다.
- [@NotBlank][notblank] - null이 아니고 최소한 하나의 공백이 아닌 문자가 있어야 합니다.
- [@Digits][digits] - 허용 범위 내의 숫자여야 합니다.
- [@Past][past] - 과거의 순간, 날짜 또는 시간이어야 합니다.
- [@Future][future] - 미래의 순간, 날짜 또는 시간이어야 합니다.
- ...

## 스프링 부트

- [@SpringBootConfiguration][springbootconfiguration] - Spring Boot 애플리케이션 `@Configuration`을 나타냅니다.
- [@EnableAutoConfiguration][enableautoconfiguration] - 클래스 경로를 기반으로 필요한 빈을 제공하기 위해 애플리케이션 컨텍스트 자동 구성을 활성화합니다.
- [@ConfigurationProperties][configurationproperties] - 키 값 속성의 외부 바인딩을 제공합니다.
- [@ConstructorBinding][constructorbinding] - 세터 대신 생성자를 사용하여 속성을 바인딩합니다.
- [@ConfigurationPropertiesScan][configurationpropertiesscan] - `@ConfigurationProperties` 클래스를 자동으로 감지합니다.
- [@SpringBootApplication][springbootapplication] - `@SpringBootConfiguration`, `@EnableAutoConfiguration`, `@ConfigurationPropertiesScan` 및 `@ComponentScan`의 조합입니다.
- [@EntityScan][entityscan] - 엔티티 클래스를 스캔할 기본 패키지를 구성합니다.
- [@EnableJpaRepositories][enablejparepositories] - JPA 리포지토리의 자동 구성을 활성화합니다.
- [@AutoConfiguration][autoconfiguration] - 새로운 자동 구성 클래스를 정의합니다.
- [@AutoConfigureBefore][autoconfigurebefore] - 지정된 자동 구성 클래스보다 먼저 자동 구성을 적용합니다.
- [@AutoConfigureAfter][autoconfigureafter] - 지정된 자동 구성 클래스 이후에 자동 구성을 적용합니다.

## 스프링 부트 테스트

- [@SpringBootTest][springboottest] - 애노테이션이 붙은 테스트 클래스는 통합 테스트를 위해 전체 애플리케이션 컨텍스트를 로드합니다.
- [@WebMvcTest][webmvctest] - 애노테이션이 붙은 테스트 클래스는 웹 레이어만 로드합니다(서비스 및 데이터 레이어는 무시됨).
- [@DataJpaTest][datajpatest] - 애노테이션이 붙은 클래스는 JPA 구성 요소만 로드합니다.
- [@JsonTest][jsontest] - 애노테이션이 붙은 클래스는 직렬화 및 역직렬화 테스트를 위해 JSON 매퍼만 로드합니다.
- [@MockBean][mockbean] - 애노테이션이 붙은 필드를 모의 객체로 표시하고 애플리케이션 컨텍스트에 빈으로 로드합니다.
- [@SpyBean][spybean] - 빈의 부분 모킹을 허용합니다.
- [@Mock][mock] - 애노테이션이 붙은 필드를 모의 객체로 정의합니다.

## 스프링 테스트

- [@ContextConfiguration][contextconfiguration] - 통합 테스트를 위해 애플리케이션 컨텍스트를 로드할 `@Configuration`을 정의합니다.
- [@ExtendWith][extendwith] - 테스트를 실행할 확장을 정의합니다(예: MockitoExtension).
- [@SpringJUnitConfig][springjunitconfig] - `@ContextConfiguration` 및 `@ExtendWith(SpringExtension.class)`를 결합합니다.
- [@TestPropertySource][testpropertysource] - 통합 테스트에 사용되는 속성 파일의 위치를 정의합니다.
- [@DirtiesContext][dirtiescontext] - 애노테이션이 붙은 테스트가 애플리케이션 컨텍스트를 더럽히고 각 테스트 후에 정리됨을 나타냅니다.
- [@ActiveProfiles][activeprofiles] - 테스트 애플리케이션 컨텍스트를 초기화할 때 로드할 활성 빈 정의를 정의합니다.
- [@Sql][sql] - 테스트 전후에 실행할 SQL 스크립트와 문을 정의할 수 있습니다.

## 트랜잭션

- [@EnableTransactionManagement][enabletransactionmanagement] - 애노테이션 기반 트랜잭션 선언 `@Transactional`을 활성화합니다.
- [@Transactional][transactional] - 애노테이션이 붙은 메서드는 트랜잭션 방식으로 실행됩니다.

## 스프링 JPA 및 하이버네이트

- [@Id][id] - 애노테이션이 붙은 필드를 엔티티의 기본 키로 표시합니다.
- [@GeneratedValue][generatedvalue] - 기본 키의 생성 전략을 제공합니다.
- [@Column][column] - 필드에 대한 추가 구성을 제공합니다(예: 열 이름).
- [@Table][table] - 엔티티에 대한 추가 구성을 제공합니다(예: 테이블 이름).
- [@PersistenceContext][persistencecontext] - `EntityManager`가 애노테이션이 붙은 세터와 필드에 주입됩니다.
- [@Embedded][embedded] - 애노테이션이 붙은 필드는 `Embeddable` 클래스의 값으로 인스턴스화됩니다.
- [@Embeddable][embeddable] - 애노테이션이 붙은 클래스의 인스턴스는 엔티티의 일부로 저장됩니다.
- [@EmbeddedId][embeddedid] - 애노테이션이 붙은 속성을 임베디드 클래스에 의해 매핑된 복합 키로 표시합니다.
- [@AttributeOverride][attributeoverride] - 필드의 기본 매핑을 재정의합니다.
- [@Transient][transient] - 애노테이션이 붙은 필드는 영속적이지 않습니다.
- [@CreationTimestamp][creationtimestamp] - 애노테이션이 붙은 필드는 엔티티가 처음 저장된 타임스탬프를 포함합니다.
- [@UpdateTimestamp][updatetimestamp] - 애노테이션이 붙은 필드는 엔티티가 마지막으로 업데이트된 타임스탬프를 포함합니다.
- [@ManyToOne][manytoone] - N:1 관계를 나타내며, 애노테이션이 붙은 필드를 포함하는 엔티티는 다른 클래스의 엔티티와 단일 관계를 가지지만 다른 클래스는 여러 관계를 가집니다.
- [@JoinColumn][joincolumn] - 소유 측의 `@ManyToOne` 또는 `@OneToOne` 관계에서 엔티티를 조인하는 열을 나타내거나 단방향 `@OneToMany`를 나타냅니다.
- [@OneToOne][onetoone] - 1:1 관계를 나타냅니다.
- [@MapsId][mapsid] - `@ManyToOne` 또는 `@OneToOne` 관계의 소유 측 조인 열을 참조하여 참조 및 참조된 엔티티의 기본 키로 만듭니다.
- [@ManyToMany][manytomany] - N:M 관계를 나타냅니다.
- [@JoinTable][jointable] - 조인 테이블을 사용한 연관을 지정합니다.
- [@BatchSize][batchsize] - 애노테이션이 붙은 엔티티 컬렉션을 지연 로드할 크기를 정의합니다.
- [@FetchMode][fetchmode] - 연관에 대한 페치 전략을 정의합니다(예: 단일 서브쿼리로 모든 엔티티 로드).

## 스프링 시큐리티

- [@EnableWebSecurity][enablewebsecurity] - 웹 보안을 활성화합니다.
- [@EnableGlobalMethodSecurity][enableglobalmethodsecurity] - 메서드 보안을 활성화합니다.
- [@PreAuthorize][preauthorize] - SpEL을 사용하여 접근 제어 표현식을 정의하며, 보호된 메서드를 호출하기 전에 평가됩니다.
- [@PostAuthorize][postauthorize] - SpEL을 사용하여 접근 제어 표현식을 정의하며, 보호된 메서드를 호출한 후 평가됩니다.
- [@RolesAllowed][rolesallowed] - 보호된 메서드를 호출할 수 있는 보안 역할 목록을 지정합니다.

## 스프링 AOP

- [@EnableAspectJAutoProxy][enableaspectjautoproxy] - `@Aspect`로 표시된 구성 요소를 처리하는 지원을 활성화합니다.
- [@Aspect][aspect] - 애노테이션이 붙은 구성 요소를 포인트컷과 어드바이스를 포함하는 측면으로 선언합니다.
- [@Before][before] - 호출이 조인 포인트로 전파되기 전에 실행되는 포인트컷을 선언합니다.
- [@AfterReturning][afterreturning] - 조인 포인트가 성공적으로 결과를 반환하면 실행되는 포인트컷을 선언합니다.
- [@AfterThrowing][afterthrowing] - 조인 포인트가 예외를 던지면 실행되는 포인트컷을 선언합니다.
- [@After][after] - 조인 포인트가 성공적으로 결과를 반환하거나 예외를 던지면 실행되는 포인트컷을 선언합니다.
- [@Around][around] - 호출 전에 실행되는 포인트컷을 선언하여 조인 포인트의 실행을 어드바이스에 제어를 넘깁니다.

## 유용한 링크
- [Spring 공식 문서](https://docs.spring.io/spring-framework/reference/)
- [Spring Boot 참조 가이드](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/)
- [Spring Security 문서](https://docs.spring.io/spring-security/reference/)
- [Spring Data JPA 문서](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods)
- [Baeldung Spring 튜토리얼](https://www.baeldung.com/spring-tutorial)
- [Spring 깃허브 저장소](https://github.com/spring-projects/spring-framework)



[shield-prs]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg
[shield-license]: https://img.shields.io/badge/license-CC0-green

[bean]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Bean.html
[primary]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Primary.html
[component]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/stereotype/Component.html
[controller]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/stereotype/Controller.html
[rest-controller]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html
[config]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Configuration.html
[service]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/stereotype/Service.html
[repo]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/stereotype/Repository.html

[postconstruct]: https://javaee.github.io/javaee-spec/javadocs/javax/annotation/PostConstruct.html
[predestroy]: https://javaee.github.io/javaee-spec/javadocs/javax/annotation/PreDestroy.html

[import]:https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Import.html
[propertysource]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/PropertySource.html
[value]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/annotation/Value.html
[componentscan]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/ComponentScan.html

[lazy]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Lazy.html
[profile]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Profile.html 
[scope]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Scope.html
[dependson]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/DependsOn.html
[order]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/core/annotation/Order.html
[primary]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Primary.html
[conditional]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Conditional.html
[conditionalonbean]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/condition/ConditionalOnBean.html
[conditionalonmissingbean]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/condition/ConditionalOnMissingBean.html
[conditionalonclass]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/condition/ConditionalOnClass.html
[conditionalonmissingclass]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/condition/ConditionalOnMissingClass.html
[conditionalonproperty]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/condition/ConditionalOnProperty.html
[conditionalonmissingproperty]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/condition/ConditionalOnProperty.html

[autowired]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html
[qualifier]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/annotation/Qualifier.html

[valid]: https://javaee.github.io/javaee-spec/javadocs/javax/validation/Valid.html
[validated]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/validation/annotation/Validated.html
[notnull]: https://javaee.github.io/javaee-spec/javadocs/javax/validation/constraints/NotNull.html
[notempty]: https://javaee.github.io/javaee-spec/javadocs/javax/validation/constraints/NotEmpty.html
[notblank]: https://javaee.github.io/javaee-spec/javadocs/javax/validation/constraints/NotBlank.html
[digits]: https://javaee.github.io/javaee-spec/javadocs/javax/validation/constraints/Digits.html
[past]: https://javaee.github.io/javaee-spec/javadocs/javax/validation/constraints/Past.html
[future]: https://javaee.github.io/javaee-spec/javadocs/javax/validation/constraints/Future.html


[springbootconfiguration]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/SpringBootConfiguration.html
[enableautoconfiguration]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/EnableAutoConfiguration.html
[configurationproperties]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/context/properties/ConfigurationProperties.html
[constructorbinding]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/context/properties/ConstructorBinding.html
[configurationpropertiesscan]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/context/properties/ConfigurationPropertiesScan.html
[springbootapplication]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/SpringBootApplication.html
[entityscan]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/domain/EntityScan.html
[enablejparepositories]: https://docs.spring.io/spring-data/data-jpa/docs/current/api/org/springframework/data/jpa/repository/config/EnableJpaRepositories.html

[springboottest]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/context/SpringBootTest.html
[webmvctest]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/autoconfigure/web/servlet/WebMvcTest.html
[datajpatest]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/autoconfigure/orm/jpa/DataJpaTest.html
[jsontest]: https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.testing.spring-boot-applications.json-tests
[mockbean]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/mock/mockito/MockBean.html
[spybean]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/mock/mockito/SpyBean.html
[mock]: https://www.javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mock.html

[contextconfiguration]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/test/context/ContextConfiguration.html
[extendwith]: https://junit.org/junit5/docs/current/api/org.junit.jupiter.api/org/junit/jupiter/api/extension/ExtendWith.html
[springjunitconfig]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/test/context/junit/jupiter/SpringJUnitConfig.html
[testpropertysource]: https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/test/context/TestPropertySource.html
[dirtiescontext]: https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/test/annotation/DirtiesContext.html
[activeprofiles]: https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/test/context/ActiveProfiles.html
[sql]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/test/context/jdbc/Sql.html

[enabletransactionmanagement]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/EnableTransactionManagement.html
[transactional]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Transactional.html

[id]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/Id.html
[generatedvalue]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/GeneratedValue.html
[entity]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/Entity.html
[column]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/Column.html
[table]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/Table.html
[persistencecontext]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/PersistenceContext.html
[embedded]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/Embedded.html
[embeddable]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/Embeddable.html
[embeddedid]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/EmbeddedId.html
[attributeoverride]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/AttributeOverride.html
[transient]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/Transient.html
[creationtimestamp]: https://docs.jboss.org/hibernate/orm/5.4/javadocs/org/hibernate/annotations/CreationTimestamp.html
[updatetimestamp]: https://docs.jboss.org/hibernate/orm/5.4/javadocs/org/hibernate/annotations/UpdateTimestamp.html
[manytoone]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/ManyToOne.html
[joincolumn]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/JoinColumn.html
[onetoone]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/OneToOne.html
[mapsid]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/MapsId.html
[manytomany]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/ManyToMany.html
[jointable]: https://javaee.github.io/javaee-spec/javadocs/javax/persistence/JoinTable.html
[batchsize]: https://docs.jboss.org/hibernate/orm/5.4/javadocs/org/hibernate/annotations/BatchSize.html
[fetchmode]: https://docs.jboss.org/hibernate/orm/5.4/javadocs/org/hibernate/annotations/FetchMode.html

[enablewebsecurity]:https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/config/annotation/web/configuration/EnableWebSecurity.html
[enableglobalmethodsecurity]: https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/config/annotation/method/configuration/EnableGlobalMethodSecurity.html
[preauthorize]: https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/access/prepost/PreAuthorize.html
[postauthorize]: https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/access/prepost/PostAuthorize.html
[rolesallowed]: https://javaee.github.io/javaee-spec/javadocs/javax/annotation/security/RolesAllowed.html
[secured]: https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/access/annotation/Secured.html

[enableaspectjautoproxy]: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/EnableAspectJAutoProxy.html
[aspect]: https://javadoc.io/static/org.aspectj/aspectjrt/1.9.5/org/aspectj/lang/annotation/Aspect.html
[before]: https://javadoc.io/static/org.aspectj/aspectjrt/1.9.5/org/aspectj/lang/annotation/Before.html
[afterreturning]: https://javadoc.io/static/org.aspectj/aspectjrt/1.9.5/org/aspectj/lang/annotation/AfterReturning.html
[afterthrowing]: https://javadoc.io/static/org.aspectj/aspectjrt/1.9.5/org/aspectj/lang/annotation/AfterThrowing.html
[after]: https://javadoc.io/static/org.aspectj/aspectjrt/1.9.5/org/aspectj/lang/annotation/After.html
[around]: https://javadoc.io/static/org.aspectj/aspectjrt/1.9.5/org/aspectj/lang/annotation/Around.html
[pointcut]: https://javadoc.io/static/org.aspectj/aspectjrt/1.9.5/org/aspectj/lang/annotation/Pointcut.html

[autoconfiguration]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/AutoConfiguration.html
[autoconfigurebefore]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/AutoConfigureBefore.html
[autoconfigureafter]: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/AutoConfigureAfter.html

