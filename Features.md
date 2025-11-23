# Features

### 1. Data Upload & Management

- **CSV File Upload**: Support for chemical equipment parameter datasets
- **Automatic Validation**: Column validation (Equipment Name, Type, Flowrate, Pressure, Temperature)
- **History Management**: Automatic retention of last 5 datasets per user
- **File Storage**: Secure server-side storage with organized directory structure
- **Concurrent Processing**: Multiple datasets can be processed simultaneously

### 2. Multi-Phase Analysis Pipeline

#### Phase 1: Column Profiling & AI Suggestions (15-30 seconds)
- Column type detection (numeric, categorical, datetime)
- Missing value analysis
- Unique value counting
- Basic statistics computation
- **AI-Generated Suggestions**: Gemini API analyzes column profiles and provides actionable recommendations

#### Phase 2: Deep Statistical Analysis (10-20 seconds)
- **Enhanced Summary Statistics**:
  - Mean, Median, Mode
  - Standard Deviation, Variance
  - Quartiles (Q1, Q3), Interquartile Range (IQR)
  - Min, Max, Range
  - Skewness, Kurtosis
- **Outlier Detection**: IQR-based method with severity classification
- **Correlation Analysis**: Pearson correlation matrix for all numeric parameters
- **Categorical Distribution**: Frequency analysis for equipment types

#### Phase 3: AI Insights Generation (20-40 seconds)
- **Executive Summary**: High-level analysis of key findings
- **Trend Identification**: Pattern recognition in operational parameters
- **Anomaly Explanations**: AI-powered outlier interpretation
- **Optimization Recommendations**: Process improvement suggestions
- **Risk Assessment**: Potential equipment failure predictions

### 3. Real-Time Updates

- **WebSocket Integration**: Instant notifications for processing status changes
- **Progress Tracking**: Phase-by-phase completion updates
- **Auto-Refresh**: Frontend automatically updates when analysis completes
- **Status Indicators**: Visual feedback for PROCESSING, PROFILING, ANALYZING, AI_PROCESSING, COMPLETED, FAILED

### 4. Statistical Visualization

#### Web Dashboard
- **Type Distribution Chart**: Bar chart showing equipment count by type
- **Equipment Proportion**: Doughnut chart for percentage breakdown
- **Parameter Correlation**: Scatter plot (Flowrate vs Pressure, colored by Temperature)
- **Correlation Heatmap**: Interactive heatmap with coefficient display
- **Outlier Explorer**: Table with deviation percentages and AI explanations
- **Statistical Summary Table**: Comprehensive stats for all numeric parameters

#### Desktop Application
- **Stats Cards**: Large, readable metric displays (Total Records, Avg Pressure, Avg Temperature, Status)
- **Data Table**: Paginated view of raw dataset
- **AI Insights Panel**: Formatted display of executive summary and suggestions

### 5. AI-Powered Features

#### Smart Suggestions (Phase 1)
- Data quality recommendations
- Column-specific insights
- Missing data handling strategies
- Feature engineering suggestions

#### Executive Summary (Phase 3)
- Dataset overview with key statistics
- Primary findings and trends
- Critical issues identification
- Overall data quality assessment

#### Outlier Explanations
- Per-outlier AI-generated explanations
- Contextual analysis considering equipment type and parameter
- Potential root cause identification
- Recommended corrective actions

#### Optimization Recommendations
- Process efficiency improvements
- Equipment operation optimization
- Predictive maintenance suggestions
- Safety enhancement recommendations

### 6. Performance Optimization

#### Redis Caching System
- **Cache Strategy**: MD5 hash-based keys with prefix organization
- **Smart TTLs**:
  - Suggestions: 24 hours (structural data)
  - Summaries: 12 hours (aggregated data)
  - Explanations: 1 hour (specific queries)
  - Optimizations: 2 hours (recommendation data)
- **Performance Gain**: 600x faster for cached responses (<100ms vs 20-40s)
- **Cache Warming**: Pre-population support for frequently accessed data
- **Invalidation**: Dataset-specific cache clearing on updates

### 7. Enhanced PDF Reports

- **Professional Layout**: Multi-page report with sections
- **Cover Page**: Dataset summary with total records and analysis date
- **Executive Summary**: AI-generated insights on dedicated page
- **Statistical Overview**: Tables with mean, median, std, quartiles
- **Embedded Visualizations**:
  - Equipment distribution bar chart
  - Parameter correlation scatter plots
  - Correlation heatmap (Seaborn)
  - Parameter ranges comparison chart
- **Outlier Analysis**: Tables with deviation percentages and severity indicators
- **Color-Coded Sections**: Professional styling with headers and borders
- **Downloadable Format**: One-click download from web or desktop app

### 8. Authentication & Security

- **JWT Authentication**: Secure token-based authentication
- **Token Refresh**: Automatic access token renewal
- **User Registration**: Self-service account creation
- **Password Security**: Hashed password storage
- **Authorization**: User-specific dataset access control
- **CORS Configuration**: Secure cross-origin resource sharing

---