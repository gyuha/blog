---
title: "OpenRAG: Langflow 기반 통합 RAG 플랫폼"
date: 2026-03-12T17:00:00+09:00
draft: false
categories:
  - AI/ML
  - RAG
tags:
  - RAG
  - Langflow
  - OpenSearch
  - Docling
  - MCP
  - AI
  - Vector Database
description: "OpenRAG는 Langflow, OpenSearch, Docling을 통합한 사전 패키징된 RAG 플랫폼으로, 시각적 워크플로우 빌더와 엔터프라이즈급 시맨틱 검색을 제공합니다."
---

OpenRAG는 문서 지식 기반 AI 응용 프로그램을 구축하기 위한 종합적인 RAG(Retrieval-Augmented Generation) 플랫폼입니다. Langflow의 시각적 워크플로우 빌더, OpenSearch의 확장 가능한 검색 엔진, Docling의 강력한 문서 처리 기능을 하나로 통합하여 개발자가 복잡한 RAG 시스템을 신속하게 구축할 수 있도록 지원합니다.

이 글에서는 OpenRAG의 핵심 아키텍처, 주요 기능, 그리고 실제 구현 방법을 살펴보겠습니다.

<!--more-->

## Sources

- [OpenRAG GitHub Repository](https://github.com/langflow-ai/openrag)
- [Langflow Documentation](https://langflow.org)
- [OpenSearch Documentation](https://opensearch.org)
- [Docling Documentation](https://github.com/docling-project/docling)

## RAG 아키텍처 이해

RAG(Retrieval-Augmented Generation)는 대규모 언어 모델(LLM)의 응답 품질을 향상시키기 위해 외부 지식 베이스에서 관련 정보를 검색하여 컨텍스트에 포함하는 패턴입니다. 전통적인 RAG 아키텍처는 다음과 같은 구성 요소로 이루어집니다.

```mermaid
flowchart TD
    subgraph Input["입력 계층"]
        UQ[사용자 질의]
    end

    subgraph Retrieval["검색 계층"]
        QE[쿼리 임베딩]
        VDB[벡터 데이터베이스]
        VS[벡터 유사도 검색]
    end

    subgraph Processing["처리 계층"]
        CR[컨텍스트 재구성]
        PM[프롬프트 템플릿]
    end

    subgraph Generation["생성 계층"]
        LLM[언어 모델]
        AR[AI 응답]
    end

    UQ --> QE
    QE --> VS
    VDB --> VS
    VS --> CR
    CR --> PM
    PM --> LLM
    LLM --> AR

    classDef inputStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef retrievalStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef processingStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef generationStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333

    class UQ inputStyle
    class QE,VS,VDB retrievalStyle
    class CR,PM processingStyle
    class LLM,AR generationStyle
```

### 기본 RAG 패턴

기본 RAG 패턴은 사용자 질의를 임베딩하고, 벡터 데이터베이스에서 유사한 문서 청크를 검색한 후, 이를 LLM 프롬프트에 컨텍스트로 제공합니다.

### 하이브리드 검색 RAG

하이브리드 검색 RAG는 밀도 높은 벡터 유사도 검색과 키워드 기반 검색(BM25)을 결합하여 검색 정확도를 높입니다. 이는 의미적 유사성과 정확한 키워드 매칭을 모두 활용합니다.

```mermaid
flowchart LR
    Q[사용자 질의] --> QE[쿼리 임베딩]
    Q --> KQ[키워드 추출]

    QE --> VS[벡터 검색]
    KQ --> KS[키워드 검색]

    VS --> RR[결합 리랭킹]
    KS --> RR

    RR --> LLM[LLM 생성]

    classDef queryStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef vectorStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef keywordStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333
    classDef rerankStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef llmStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333

    class Q queryStyle
    class QE,VS vectorStyle
    class KQ,KS keywordStyle
    class RR rerankStyle
    class LLM llmStyle
```

### 에이전트 RAG

에이전트 RAG는 단순 검색을 넘어, 에이전트가 검색 여부를 결정하고 다단계 검색을 수행할 수 있도록 합니다. 이를 통해 더 복잡한 질의에 대해 반복적 검색과 추론이 가능합니다.

```mermaid
flowchart TD
    Q[사용자 질의] --> AD[에이전트 결정]

    AD -->|검색 필요| R1[1차 검색]
    AD -->|직접 응답| LLM1[LLM 응답]

    R1 --> Eval[결과 평가]

    Eval -->|불충분| R2[2차 검색]
    Eval -->|충분| LLM2[LLM 응답]

    R2 --> LLM2

    classDef queryStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef agentStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333
    classDef searchStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef evalStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef llmStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333

    class Q queryStyle
    class AD agentStyle
    class R1,R2 searchStyle
    class Eval evalStyle
    class LLM1,LLM2 llmStyle
```

## OpenRAG 핵심 아키텍처

OpenRAG는 다음과 같은 핵심 구성 요소로 이루어진 통합 플랫폼을 제공합니다.

```mermaid
flowchart TB
    subgraph Ingestion["문서 수집 계층"]
        PDF[PDF 문서]
        DOCX[DOCX 문서]
        PPTX[PPTX 문서]
        IMG[이미지]
        DL[Docling 파서]
        Chunk[청킹 처리]
    end

    subgraph Embedding["임베딩 계층"]
        Model[임베딩 모델]
        Vector[벡터화]
    end

    subgraph Storage["저장소 계층"]
        OS[OpenSearch]
        Index[인덱스 관리]
    end

    subgraph Workflow["워크플로우 계층"]
        LF[Langflow]
        UI[드래그 앤 드롭 UI]
    end

    subgraph API["API 계층"]
        PY[Python SDK]
        TS[TypeScript SDK]
        MCP[MCP 서버]
    end

    PDF --> DL
    DOCX --> DL
    PPTX --> DL
    IMG --> DL

    DL --> Chunk
    Chunk --> Model
    Model --> Vector
    Vector --> OS
    OS --> Index

    UI --> LF
    LF --> OS

    PY --> OS
    TS --> OS
    MCP --> OS

    classDef docStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef processStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef storageStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef workflowStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333
    classDef apiStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333

    class PDF,DOCX,PPTX,IMG docStyle
    class DL,Chunk,Model,Vector processStyle
    class OS,Index storageStyle
    class LF,UI workflowStyle
    class PY,TS,MCP apiStyle
```

## Langflow 시각적 워크플로우 빌더

OpenRAG의 핵심 특징 중 하나는 Langflow 기반의 시각적 워크플로우 빌더입니다. Langflow는 개발자가 코드를 작성하지 않고도 드래그 앤 드롭 방식으로 복잡한 AI 워크플로우를 구성할 수 있게 해줍니다.

### Langflow 워크플로우 구성 요소

```mermaid
flowchart LR
    subgraph Components["Langflow 구성 요소"]
        INP[입력 노드]
        PROC[처리 노드]
        RET[검색 노드]
        LLM[LLM 노드]
        OUT[출력 노드]
    end

    INP --> PROC
    PROC --> RET
    RET --> LLM
    LLM --> OUT

    classDef nodeStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333

    class INP,PROC,RET,LLM,OUT nodeStyle
```

### 문서 수집 워크플로우

Langflow를 사용하면 문서 수집 파이프라인을 시각적으로 설계할 수 있습니다.

```mermaid
flowchart TD
    subgraph Upload["업로드 단계"]
        UF[파일 업로드]
        FD[형식 감지]
    end

    subgraph Parse["파싱 단계"]
        DP[Docling 파서]
        TX[텍스트 추출]
        TB[표 감지]
        IM[이미지 추출]
    end

    subgraph Process["처리 단계"]
        CH[청킹]
        MT[메타데이터 추출]
    end

    subgraph Index["인덱싱 단계"]
        EB[임베딩]
        IDX[OpenSearch 인덱싱]
    end

    UF --> FD
    FD --> DP
    DP --> TX
    DP --> TB
    DP --> IM

    TX --> CH
    TB --> CH
    IM --> CH

    CH --> MT
    MT --> EB
    EB --> IDX

    classDef uploadStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef parseStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef processStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef indexStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class UF,FD uploadStyle
    class DP,TX,TB,IM parseStyle
    class CH,MT processStyle
    class EB,IDX indexStyle
```

### RAG 검색 워크플로우

검색 및 생성 워크플로우 역시 시각적으로 구성할 수 있습니다.

```mermaid
flowchart TD
    subgraph Query["질의 처리"]
        QIN[질의 입력]
        QR[질의 리라이팅]
    end

    subgraph Retrieval["검색 처리"]
        QE[쿼리 임베딩]
        HYB[하이브리드 검색]
        RER[리랭킹]
    end

    subgraph Generation["생성 처리"]
        CT[컨텍스트 구성]
        PG[프롬프트 생성]
        LLM[LLM 호출]
    end

    subgraph Output["출력 처리"]
        REF[참조 문서]
        RES[최종 응답]
    end

    QIN --> QR
    QR --> QE
    QE --> HYB
    HYB --> RER
    RER --> CT
    CT --> PG
    PG --> LLM
    LLM --> RES
    RER --> REF

    classDef queryStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef retrievalStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef generationStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef outputStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class QIN,QR queryStyle
    class QE,HYB,RER retrievalStyle
    class CT,PG,LLM generationStyle
    class REF,RES outputStyle
```

## OpenSearch 엔터프라이즈 검색

OpenRAG는 OpenSearch를 기본 검색 엔진으로 사용합니다. OpenSearch는 확장 가능한 오픈 소스 검색 및 분석 엔진으로, 엔터프라이즈급 시맨틱 검색 기능을 제공합니다.

### OpenSearch k-NN 플러그인

OpenSearch의 k-NN(k-Nearest Neighbors) 플러그인은 벡터 유사도 검색을 위한 고성능 엔진을 제공합니다.

```mermaid
flowchart LR
    subgraph VectorSearch["벡터 검색 처리"]
        QV[쿼리 벡터]
        IV[인덱스 벡터]
        KNN[k-NN 알고리즘]
        TOP[Top-K 결과]
    end

    QV --> KNN
    IV --> KNN
    KNN --> TOP

    classDef inputStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef indexStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef algoStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef resultStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class QV inputStyle
    class IV indexStyle
    class KNN algoStyle
    class TOP resultStyle
```

### 하이브리드 검색 구현

OpenSearch는 벡터 검색과 키워드 검색을 결합한 하이브리드 검색을 지원합니다.

```mermaid
flowchart TD
    Q[사용자 질의] --> 분기{검색 유형}

    분기 -->|벡터| VS[벡터 검색]
    분기 -->|키워드| KS[BM25 검색]

    VS --> RRF[Reciprocal Rank Fusion]
    KS --> RRF

    RRF --> 최종[결과 병합]

    classDef queryStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef vectorStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef keywordStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333
    classDef fusionStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef resultStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333

    class Q queryStyle
    class VS vectorStyle
    class KS keywordStyle
    class RRF fusionStyle
    class 최종 resultStyle
```

### 확장성

OpenSearch의 수평 확장 기능을 통해 대규모 문서 세트도 효율적으로 처리할 수 있습니다.

```mermaid
flowchart LR
    subgraph Cluster["OpenSearch 클러스터"]
        M1[마스터 노드 1]
        M2[마스터 노드 2]
        M3[마스터 노드 3]

        D1[데이터 노드 1]
        D2[데이터 노드 2]
        D3[데이터 노드 3]

        C1[조정 노드 1]
        C2[조정 노드 2]
    end

    M1 --- M2
    M2 --- M3
    M3 --- M1

    M1 --- D1
    M2 --- D2
    M3 --- D3

    M1 --- C1
    M2 --- C2

    classDef masterStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333
    classDef dataStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef coordStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class M1,M2,M3 masterStyle
    class D1,D2,D3 dataStyle
    class C1,C2 coordStyle
```

## Docling 문서 처리

Docling은 PDF, DOCX, PPTX, 이미지 등 다양한 형식의 문서를 처리하는 강력한 파이썬 라이브러리입니다. OpenRAG는 Docling을 통해 문서 수집 파이프라인을 제공합니다.

### 지원 문서 형식

```mermaid
flowchart TD
    Docs[입력 문서] --> PDF[PDF]
    Docs --> DOCX[Microsoft Word]
    Docs --> PPTX[Microsoft PowerPoint]
    Docs --> IMG[이미지]

    PDF --> Docling[Docling 파서]
    DOCX --> Docling
    PPTX --> Docling
    IMG --> Docling

    Docling --> Text[텍스트 추출]
    Docling --> Table[표 감지]
    Docling --> Meta[메타데이터]

    Text --> Chunk[청킹]
    Table --> Chunk
    Meta --> Chunk

    classDef docStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef parserStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef extractStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef chunkStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class PDF,DOCX,PPTX,IMG docStyle
    class Docling parserStyle
    class Text,Table,Meta extractStyle
    class Chunk chunkStyle
```

### 레이아웃 이해

Docling은 문서의 레이아웃 구조를 이해하여 표, 이미지, 제목 등을 정확하게 식별할 수 있습니다.

```mermaid
flowchart LR
    Raw[원시 문서] --> Layout[레이아웃 분석]

    Layout --> 제목[제목 식별]
    Layout --> 문단[문단 식별]
    Layout --> 표[표 감지]
    Layout --> 그림[그림 감지]

    제목 --> 구조[구조화된 출력]
    문단 --> 구조
    표 --> 구조
    그림 --> 구조

    classDef inputStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef processStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef elementStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef outputStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class Raw inputStyle
    class Layout processStyle
    class 제목,문단,표,그림 elementStyle
    class 구조 outputStyle
```

## MCP 통합

OpenRAG는 MCP(Model Context Protocol)를 통해 AI 개발 환경과 통합될 수 있습니다.

### Cursor IDE 통합

Cursor IDE에서 OpenRAG MCP 서버를 구성하면, 코드 작성 중 문서 검색 및 AI 응답을 직접 활용할 수 있습니다.

```json
{
  "mcpServers": {
    "openrag": {
      "command": "uvx",
      "args": ["openrag-mcp"],
      "env": {
        "OPENRAG_URL": "http://localhost:3000",
        "OPENRAG_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Claude Desktop 통합

Claude Desktop에서도 동일한 MCP 구성을 사용하여 로컬 문서 검색 및 AI 응답을 활용할 수 있습니다.

```mermaid
flowchart LR
    subgraph Client["AI 클라이언트"]
        CUR[Cursor IDE]
        CLD[Claude Desktop]
    end

    subgraph MCP["MCP 서버"]
        OMC[openrag-mcp]
    end

    subgraph OpenRAG["OpenRAG 서버"]
        API[API 서버]
        OS[OpenSearch]
    end

    CUR --> OMC
    CLD --> OMC
    OMC --> API
    API --> OS

    classDef clientStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef mcpStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef serverStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef storageStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class CUR,CLD clientStyle
    class OMC mcpStyle
    class API serverStyle
    class OS storageStyle
```

## SDK 사용

OpenRAG는 Python과 TypeScript/JavaScript SDK를 공식적으로 제공합니다.

### Python SDK

```python
import asyncio
from openrag_sdk import OpenRAGClient

async def main():
    async with OpenRAGClient() as client:
        response = await client.chat.create(message="RAG이란 무엇인가?")
        print(response.response)

if __name__ == "__main__":
    asyncio.run(main())
```

### TypeScript SDK

```typescript
import { OpenRAGClient } from "openrag-sdk";

const client = new OpenRAGClient();

async function main() {
  const response = await client.chat.create({
    message: "RAG이란 무엇인가?"
  });
  console.log(response.response);
}

main();
```

### SDK 아키텍처

```mermaid
flowchart TD
    subgraph Client["클라이언트 애플리케이션"]
        APP[사용자 앱]
    end

    subgraph SDK["SDK 계층"]
        PY[Python SDK]
        TS[TypeScript SDK]
    end

    subgraph API["API 계층"]
        REST[REST API]
        WS[WebSocket]
    end

    subgraph Core["OpenRAG 코어"]
        Chat[채팅 엔드포인트]
        Doc[문서 엔드포인트]
        Search[검색 엔드포인트]
    end

    APP --> PY
    APP --> TS

    PY --> REST
    TS --> REST

    PY --> WS
    TS --> WS

    REST --> Chat
    REST --> Doc
    REST --> Search

    WS --> Chat

    classDef appStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef sdkStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef apiStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef coreStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class APP appStyle
    class PY,TS sdkStyle
    class REST,WS apiStyle
    class Chat,Doc,Search coreStyle
```

## 에이전트 워크플로우

OpenRAG는 고급 에이전트 워크플로우 기능을 지원합니다. 이를 통해 복잡한 질의에 대해 다단계 검색과 추론이 가능합니다.

### 에이전트 검색 흐름

```mermaid
flowchart TD
    Q[사용자 질의] --> 분석[질의 분석]

    분석 --> 단순{단순 질의?}

    단순 -->|예| 직접[직접 검색]
    단순 -->|아니오| 분해[질의 분해]

    분해 --> S1[하위 질의 1]
    분해 --> S2[하위 질의 2]
    분해 --> S3[하위 질의 3]

    직접 --> R1[검색 1]
    S1 --> R2[검색 2]
    S2 --> R3[검색 3]
    S3 --> R4[검색 4]

    R1 --> 평가[결과 평가]
    R2 --> 평가
    R3 --> 평가
    R4 --> 평가

    평가 -->|불충분| 추가[추가 검색]
    평가 -->|충분| 합성[응답 합성]

    추가 --> 합성
    합성 --> OUT[최종 응답]

    classDef queryStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef analysisStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef searchStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef evalStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333
    classDef synthesisStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333

    class Q queryStyle
    class 분석,분해,단순 analysisStyle
    class 직접,S1,S2,S3,R1,R2,R3,R4,추가 searchStyle
    class 평가 evalStyle
    class 합성,OUT synthesisStyle
```

### 리랭킹

검색 결과의 품질을 향상시키기 위해 리랭킹 단계를 적용할 수 있습니다.

```mermaid
flowchart LR
    검색[검색 결과] --> 후보[후보 문서]

    후보 --> R1[리랭커 1]
    후보 --> R2[리랭커 2]
    후보 --> R3[리랭커 3]

    R1 --> 점수[점수 병합]
    R2 --> 점수
    R3 --> 점수

    점수 --> 정렬[재정렬]
    정렬 --> 최종[최종 결과]

    classDef inputStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef rerankerStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef scoreStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef outputStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333

    class 검색,후보 inputStyle
    class R1,R2,R3 rerankerStyle
    class 점수,정렬 scoreStyle
    class 최종 outputStyle
```

## 배포 및 확장

OpenRAG는 `uv` 패키지 매니저를 사용하여 간편하게 실행할 수 있으며, 컨테이너화를 통해 쉽게 배포할 수 있습니다.

### 실행 방법

```bash
# uv를 사용한 실행
uvx openrag

# 또는 직접 설치 후 실행
pip install openrag
openrag serve
```

### 아키텍처 확장

```mermaid
flowchart TB
    subgraph Frontend["프론트엔드 계층"]
        UI[Langflow UI]
        API[REST API]
    end

    subgraph Application["애플리케이션 계층"]
        App1[앱 인스턴스 1]
        App2[앱 인스턴스 2]
        App3[앱 인스턴스 3]
    end

    subgraph Cache["캐시 계층"]
        Redis[Redis]
    end

    subgraph Search["검색 계층"]
        OSCluster[OpenSearch 클러스터]
    end

    subgraph Storage["저장소 계층"]
        S3[S3 / MinIO]
    end

    UI --> API
    API --> App1
    API --> App2
    API --> App3

    App1 --> Redis
    App2 --> Redis
    App3 --> Redis

    App1 --> OSCluster
    App2 --> OSCluster
    App3 --> OSCluster

    App1 --> S3
    App2 --> S3
    App3 --> S3

    classDef frontendStyle fill:#c5dcef,stroke:#333,stroke-width:2px,color:#333
    classDef appStyle fill:#c0ecd3,stroke:#333,stroke-width:2px,color:#333
    classDef cacheStyle fill:#fde8c0,stroke:#333,stroke-width:2px,color:#333
    classDef searchStyle fill:#e0c8ef,stroke:#333,stroke-width:2px,color:#333
    classDef storageStyle fill:#ffc8c4,stroke:#333,stroke-width:2px,color:#333

    class UI,API frontendStyle
    class App1,App2,App3 appStyle
    class Redis cacheStyle
    class OSCluster searchStyle
    class S3 storageStyle
```

## 핵심 요약

```mermaid
mindmap
  root((OpenRAG))
    핵심_기능
      사전_패키징된_RAG
      Langflow_시각적_빌더
      OpenSearch_시맨틱_검색
      Docling_문서_처리
      MCP_통합
      Python_/_TypeScript_SDK
    아키텍처
      문서_수집_계층
      임베딩_계층
      OpenSearch_저장소
      Langflow_워크플로우
      API_계층
    RAG_패턴
      기본_RAG
      하이브리드_검색
      에이전트_RAG
      다단계_검색
    통합
      Cursor_IDE
      Claude_Desktop
      Python_SDK
      TypeScript_SDK
```

| 기능 | 설명 | 기술 |
|------|------|------|
| 문서 수집 | PDF, DOCX, PPTX, 이미지 처리 | Docling |
| 시맨틱 검색 | 벡터 기반 유사도 검색 | OpenSearch k-NN |
| 하이브리드 검색 | 벡터 + 키워드 결합 | BM25 + 리랭킹 |
| 시각적 빌더 | 드래그 앤 드롭 워크플로우 | Langflow |
| AI 통합 | MCP 프로토콜 지원 | Cursor, Claude Desktop |
| SDK | 공식 개발 키트 | Python, TypeScript |

## 결론

OpenRAG는 RAG 애플리케이션 개발을 위한 종합적인 플랫폼입니다. Langflow의 시각적 워크플로우 빌더를 통해 복잡한 RAG 파이프라인을 직관적으로 구성할 수 있으며, OpenSearch의 확장 가능한 검색 엔진과 Docling의 강력한 문서 처리 기능이 결합되어 엔터프라이즈급 솔루션을 제공합니다.

MCP를 통한 Cursor 및 Claude Desktop 통합은 개발 생산성을 크게 향상시키며, Python과 TypeScript SDK는 다양한 개발 환경에서 쉽게 활용할 수 있습니다. 에이전트 워크플로우와 리랭킹 같은 고급 기능을 통해 더 정교한 AI 응용 프로그램을 구축할 수 있습니다.

OpenRAG를 활용하면 개발자는 복잡한 RAG 시스템을 신속하게 구축하고, 문서 지식 기반 AI 서비스를 효율적으로 제공할 수 있습니다.
