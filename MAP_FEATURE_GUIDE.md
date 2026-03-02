# Map Integration Feature Guide

## Overview

The Digital Catalyst platform now includes an interactive map feature powered by Leaflet.js, allowing users to visualize and explore Indian heritage sites geographically.

## Features

### 1. Interactive Map View
- **URL**: `/heritage/map`
- **Technology**: Leaflet.js with OpenStreetMap tiles
- **Center**: India (20.5937°N, 78.9629°E)
- **Zoom**: Adjustable from country-level to site-level detail

### 2. Custom Markers
- Color-coded by category:
  - **Temple**: Red (#FF6B6B)
  - **Fort**: Teal (#4ECDC4)
  - **Monument**: Yellow (#FFD93D)
  - **Palace**: Light Green (#A8E6CF)
  - **Cave**: Mint (#95E1D3)
  - **Default**: Red (#FF6B6B)

### 3. Rich Popups
Each marker displays:
- Heritage site name
- State and category
- Annual visitor count
- Average rating and review count (if available)
- Link to detailed site page

### 4. Advanced Filtering
- **State Filter**: Show sites from specific states
- **Category Filter**: Filter by heritage type (Temple, Fort, Monument, etc.)
- **Real-time Updates**: Filters apply instantly without page reload
- **Statistics**: Live count of visible sites

### 5. Navigation Integration
- Map link in main navigation bar
- "View on Map" button on heritage detail pages
- Breadcrumb navigation for easy return

## Database Schema Changes

### New Columns Added to `heritage_sites` Table:
```sql
latitude REAL    -- Geographic latitude (e.g., 27.1751)
longitude REAL   -- Geographic longitude (e.g., 78.0421)
```

### Migration Script
Run `add_map_coordinates.py` to:
1. Add latitude/longitude columns
2. Populate existing sites with coordinates

## Form Updates

### Add Heritage Site Form
New fields:
- **Latitude**: Decimal input with 6 decimal places
- **Longitude**: Decimal input with 6 decimal places
- Helper text explaining geographic coordinates

### Edit Heritage Site Form
Same latitude/longitude fields with pre-populated values

## API Updates

### HeritageSite.to_dict()
Now includes:
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude
- `avg_rating`: Average rating from reviews
- `review_count`: Total number of reviews
- `view_count`: Total page views
- `bookmark_count`: Total bookmarks

## Technical Implementation

### Frontend (Leaflet.js)
```javascript
// Initialize map
const map = L.map('map').setView([20.5937, 78.9629], 5);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18
}).addTo(map);

// Add markers with custom icons
const marker = L.marker([lat, lng], {
    icon: createCustomIcon(category)
}).addTo(map);
```

### Backend (Flask Route)
```python
@main_bp.route('/heritage/map')
def heritage_map():
    # Get sites with coordinates
    sites = HeritageSite.query.filter(
        HeritageSite.latitude.isnot(None),
        HeritageSite.longitude.isnot(None)
    ).all()
    
    # Serialize to JSON
    sites_json = json.dumps([site.to_dict() for site in sites])
    
    return render_template('heritage_map.html', 
                         sites=sites,
                         sites_json=sites_json)
```

## Sample Coordinates

Pre-populated heritage sites:
- **Taj Mahal**: 27.1751°N, 78.0421°E
- **Red Fort**: 28.6562°N, 77.2410°E
- **Ajanta Caves**: 20.5519°N, 75.7033°E
- **Hampi**: 15.3350°N, 76.4600°E
- **Golden Temple**: 31.6200°N, 74.8765°E
- **Konark Sun Temple**: 19.8876°N, 86.0945°E
- **Khajuraho Temples**: 24.8318°N, 79.9199°E
- **Mysore Palace**: 12.3051°N, 76.6551°E

## Usage Instructions

### For Users
1. Navigate to "Map View" from the main menu
2. Click on any marker to see site details
3. Use state/category filters to narrow results
4. Click "View Details" in popup to visit site page

### For Administrators
1. When adding/editing heritage sites, provide latitude and longitude
2. Use Google Maps or similar tools to find coordinates
3. Format: Decimal degrees (e.g., 28.6139, not 28°36'50"N)

## Performance Considerations

### Current Implementation
- **Client-side filtering**: All sites loaded at once
- **Suitable for**: Up to 1000 sites
- **Benefits**: Instant filtering, no server requests

### Future Enhancements (for larger datasets)
- Server-side clustering
- Viewport-based loading
- Tile-based marker rendering
- Search within visible area

## Browser Compatibility

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Dependencies

### Frontend
- **Leaflet.js**: 1.9.4
- **OpenStreetMap**: Tile provider
- **Bootstrap**: 5.3.0 (for UI components)

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database queries
- **SQLite**: Database with REAL type for coordinates

## Academic Notes

### Geographic Data Visualization
This implementation demonstrates:
- **Spatial Data Storage**: Latitude/longitude in relational database
- **Client-side Rendering**: JavaScript map library
- **Data Serialization**: Python objects to JSON
- **Interactive Filtering**: Real-time UI updates

### Design Patterns
- **MVC Pattern**: Model (HeritageSite), View (template), Controller (route)
- **Separation of Concerns**: Backend data, frontend visualization
- **Progressive Enhancement**: Map works without JavaScript (fallback to list)

### Complexity Analysis
- **Marker Rendering**: O(n) where n = number of sites
- **Filtering**: O(n) for each filter application
- **Map Bounds**: O(n) to calculate bounding box
- **Overall**: Linear complexity, suitable for small-medium datasets

## Troubleshooting

### Map Not Displaying
1. Check browser console for JavaScript errors
2. Verify Leaflet CSS/JS loaded (check network tab)
3. Ensure sites have valid latitude/longitude values

### Markers Not Appearing
1. Verify database has latitude/longitude data
2. Check coordinate format (decimal degrees, not DMS)
3. Ensure coordinates are within valid range (-90 to 90 for lat, -180 to 180 for lng)

### Filters Not Working
1. Check JavaScript console for errors
2. Verify button click handlers attached
3. Ensure sites_json variable properly serialized

## Future Enhancements

### Short-term
- [ ] Geocoding API integration (auto-fill coordinates from address)
- [ ] Clustering for dense areas
- [ ] Custom map styles/themes
- [ ] Export map as image

### Long-term
- [ ] Heatmap visualization (visitor density)
- [ ] Route planning between sites
- [ ] 3D terrain view
- [ ] Augmented reality integration
- [ ] Offline map support

## Credits

- **Leaflet.js**: Open-source mapping library
- **OpenStreetMap**: Community-driven map data
- **Bootstrap Icons**: Icon library
- **Digital Catalyst Team**: Implementation and integration

---

**Last Updated**: February 2026
**Version**: 1.0.0
