# Usage Guide

### Web Application

#### 1. User Registration & Login

1. Navigate to `http://localhost:5173` (development) or your production URL
2. Click "Sign Up" to create a new account
3. Provide username, email, and password
4. Click "Sign In" to authenticate
5. Access token stored securely in browser

#### 2. Upload Dataset

1. Click **"Upload CSV"** button in the dashboard
2. Select a CSV file with required columns:
   - Equipment Name
   - Type
   - Flowrate
   - Pressure
   - Temperature
3. File uploads and processing starts automatically
4. Real-time status updates appear via WebSocket
5. Notification shown when each phase completes

#### 3. View Analysis Results

##### Overview Tab
- View key statistics in card format
- Total Records: Number of equipment entries
- Avg Pressure: Average pressure across all equipment (PSI)
- Avg Temperature: Average operating temperature (°F)
- Status: Current processing state

##### Statistics Tab
- Detailed table with all numeric parameters
- Columns: Parameter, Mean, Median, Std Dev, Min, Q1, Q3, Max
- Sort and filter capabilities
- Export to CSV option

##### AI Insights Tab
- **Executive Summary**: AI-generated high-level analysis
- **Smart Suggestions**: Actionable recommendations with reasoning
- **Key Findings**: Important patterns and trends
- Auto-updates when Phase 3 completes

##### Correlations Tab
- Interactive correlation heatmap
- Color-coded coefficients (-1 to +1)
- Strong correlations highlighted
- Click cells for detailed parameter relationships

##### Outliers Tab
- Table of detected anomalies
- Equipment name, parameter, actual value, expected range
- Deviation percentage calculation
- Click "Explain" for AI-generated outlier analysis
- Severity indicators (High, Medium, Low)

##### Optimization Tab
- Process improvement recommendations
- Equipment-specific optimization suggestions
- Efficiency enhancement strategies
- Safety improvement tips
- Click "Get Recommendations" to generate (cached for 2 hours)

#### 4. Download PDF Report

1. Navigate to dataset details
2. Click **"Download Report"** button
3. PDF generated with:
   - Cover page with summary
   - Executive summary page
   - Statistical overview with graphs
   - Correlation heatmap
   - Outlier analysis tables
   - Professional formatting
4. Save to desired location

### Desktop Application

#### 1. Launch Application

```bash
# Windows
cd desktop_app
run.bat

# Linux/Mac
cd desktop_app
./run.sh
```

#### 2. Login/Signup

- **Login Tab**: Enter username and password
- **Sign Up Tab**: Create new account with username, email, password
- Click respective button to authenticate
- Token stored securely in application session

#### 3. Upload CSV File

1. Click **"📁 Upload CSV"** button in header
2. Select CSV file from file dialog
3. Progress dialog shows upload status
4. Success message confirms upload
5. Dataset appears in history sidebar

#### 4. View Dataset

1. Click on dataset in **Recent Datasets** sidebar
2. Loading dialog appears while fetching data
3. Four tabs populate with information:

   **Overview Tab**:
   - Four stat cards with large, readable values
   - Status indicator (✅ COMPLETED, ⏳ PROCESSING, etc.)
   - **"📄 Download PDF Report"** button

   **Statistics Tab**:
   - Table with all numeric parameters
   - Mean, Median, Std Dev, Min, Q1, Q3, Max columns
   - Scrollable for many parameters

   **AI Insights Tab**:
   - Executive summary text area
   - Smart suggestions section below
   - Formatted with bullets and reasoning

   **Data Tab**:
   - Raw data preview
   - Scrollable table
   - All columns visible

#### 5. Auto-Refresh Feature

- Desktop app checks for updates every 10 seconds
- Only refreshes if status is PROCESSING/PROFILING/ANALYZING/AI_PROCESSING
- Silent background update (no interruption)
- Status cards update automatically when processing completes

#### 6. Download Report

1. Ensure dataset status is COMPLETED
2. Click **"📄 Download PDF Report"** in Overview tab
3. Choose save location in file dialog
4. PDF downloads and saves
5. Success message with file path

---