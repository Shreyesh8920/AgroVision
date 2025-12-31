const data = [
  "Data Input",
  "Data Validation",
  "Feature Processing",
  "Model Prediction",
  "Recommendation Output"
];

const width = 420;
const height = 420;
const radius = 175;
const innerRadius = 80;

const svg = d3.select("#wheel")
  .append("g")
  .attr("transform", `translate(${width / 2}, ${height / 2})`);

const color = d3.scaleOrdinal()
  .domain(data)
  .range([
    "#e8f5e9",
    "#dcedc8",
    "#c5e1a5",
    "#aed581",
    "#9ccc65"
  ]);

const pie = d3.pie().sort(null).value(() => 1);

const arc = d3.arc()
  .innerRadius(innerRadius)
  .outerRadius(radius);

const arcHover = d3.arc()
  .innerRadius(innerRadius)
  .outerRadius(radius + 10);

// Draw slices
const slices = svg.selectAll(".slice")
  .data(pie(data))
  .enter()
  .append("g")
  .attr("class", "slice");

// Draw path (NO hover here)
slices.append("path")
  .attr("d", arc)
  .attr("fill", d => color(d.data))
  .attr("stroke", "#fff")
  .attr("stroke-width", 3);

// Labels
slices.append("text")
  .attr("class", "label")
  .attr("transform", d => {
    const [x, y] = arc.centroid(d);
    return `translate(${x * 0.9}, ${y * 0.9})`;
  })
  .attr("dy", "0.35em")
  .text(d => d.data);

// Hover logic (ONLY HERE)
slices
  .on("mouseover", function () {

    d3.selectAll(".slice")
      .classed("fade", true)
      .classed("active", false);

    d3.select(this)
      .classed("fade", false)
      .classed("active", true)
      .select("path")
      .transition().duration(200)
      .attr("d", arcHover);
  })
  .on("mouseout", function () {

    d3.selectAll(".slice")
      .classed("fade", false)
      .classed("active", false)
      .select("path")
      .transition().duration(200)
      .attr("d", arc);
  });


// Center circle
svg.append("circle")
  .attr("r", innerRadius - 10)
  .attr("class", "center-circle");

svg.append("text")
  .attr("class", "center-text")
  .attr("y", -4)
  .text("AI Decision");

svg.append("text")
  .attr("class", "center-text")
  .attr("y", 12)
  .text("Engine");

