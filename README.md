# Data Visualization Dashboard

A beautiful, responsive web application for visualizing CSV and Excel data with stunning interactive charts and insights.

![Dashboard Preview](https://img.shields.io/badge/Status-Ready-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## Features

- **📊 Multiple Chart Types**: Pie, Bar, Line, and Doughnut charts
- **📁 File Support**: CSV (.csv) and Excel (.xlsx, .xls) files
- **🎨 Beautiful UI**: Modern gradient design with smooth animations
- **📱 Fully Responsive**: Works perfectly on desktop, tablet, and mobile
- **🔍 Auto Analysis**: Automatically detects data patterns and creates relevant visualizations
- **📈 Real-time Stats**: Instant statistics and insights from your data
- **💾 Export Insights**: Download analysis results as JSON
- **🎯 Drag & Drop**: Easy file upload with drag-and-drop support

## Quick Start

### Option 1: Open Directly (Recommended)
Simply open `index.html` in your web browser. All dependencies are loaded via CDN, so no installation required!

### Option 2: Using a Local Server
```bash
# Install http-server (if not already installed)
npm install -g http-server

# Start the server
npm start
# or
http-server -p 8080
```

Then open your browser to `http://localhost:8080`

## How to Use

1. **Upload Your Data**
   - Click the upload area or drag and drop your CSV/Excel file
   - Supports .csv, .xlsx, and .xls formats

2. **View Visualizations**
   - The app automatically analyzes your data
   - Multiple charts are generated based on your data structure
   - Interactive tooltips show detailed information

3. **Explore Insights**
   - View key statistics at the top
   - Browse the data table preview
   - Export insights as JSON for further analysis

4. **Customize Views**
   - Use the controls to select different columns
   - Choose specific chart types
   - Filter and explore your data

## Supported Data Formats

### CSV Example
```csv
ID,Name,Status,Date,Source
1,John Doe,ACTIVE,2025-01-01,Facebook
2,Jane Smith,INACTIVE,2025-01-02,Instagram
```

### Excel
- .xlsx (Excel 2007+)
- .xls (Excel 97-2003)

## Technologies Used

- **Chart.js** - Beautiful, responsive charts
- **PapaParse** - Fast CSV parsing
- **SheetJS (XLSX)** - Excel file processing
- **Vanilla JavaScript** - No framework dependencies
- **Modern CSS** - Gradients, animations, and responsive design

## Features in Detail

### Automatic Chart Generation
The app intelligently analyzes your data and creates:
- **Status Distribution** (Pie Chart) - Shows breakdown of categorical data
- **Source Analysis** (Bar Chart) - Compares different data sources
- **Time Trends** (Line Chart) - Visualizes data over time
- **Top Contributors** (Doughnut Chart) - Highlights top performers

### Responsive Design
- Works on all screen sizes
- Touch-friendly interface
- Optimized for mobile viewing

### Data Analysis
- Automatic column detection
- Statistical summaries
- Unique value counting
- Trend identification

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## Example Use Cases

- **Sales Data**: Visualize sales by region, product, or time
- **CRM Analytics**: Analyze leads, conversions, and sources
- **Survey Results**: Display responses and statistics
- **Financial Data**: Track expenses, revenue, and trends
- **Marketing Metrics**: Monitor campaign performance
- **Inventory Management**: Track stock levels and movements

## Sample Data

The project includes a sample CRM leads dataset (`faraz analysis.csv`) that you can use to test the application.

## Customization

### Colors
Edit the color palettes in `app.js`:
```javascript
const colorPalettes = {
    vibrant: [...],
    gradient: [...]
};
```

### Chart Options
Modify chart configurations in the `create*Chart` functions in `app.js`.

### Styling
Customize the look in `styles.css` by changing CSS variables:
```css
:root {
    --primary: #6366f1;
    --secondary: #ec4899;
    /* ... */
}
```

## Performance

- Handles files up to several MB
- Efficient data processing
- Smooth animations and transitions
- Optimized rendering

## Privacy

All data processing happens locally in your browser. No data is sent to any server.

## License

MIT License - feel free to use this project for any purpose!

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ for data visualization enthusiasts
