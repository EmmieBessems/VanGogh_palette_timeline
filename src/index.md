---
toc: false
sidebar: false
theme: "wide"
---

<style>
  .tippy-box[data-theme~='custom'] {
    background-color: white;
    border: 1px solid black;
  }

  .container img {
    height: 100%;
    width: 100%;
    object-fit: contain;
  }
  
  .pigmentTable {
    display: block;
    overflow-x: scroll;
    white-space: nowrap;
  }

</style>

<div class="grid grid-cols-4">
  <div class="card">
  <h3>Search for a painting</h3>

  ```js
  // The following blocks contain all code for the user input settings, as well as accompanying code

  // Make a combination of main ID and title to ensure the unique look-up of paintings
  const titleIdArray = paintingsImages.map((d) => d.title + ", " + d.fnumber);

  // Create a search bar to look up paintings in the tool (searched paintings act as clicked paintings)
  const paintingSearch = view(Inputs.text({
    placeholder: "Catalogue nr. or (partial) title", 
    submit: true,
    datalist: titleIdArray}));
  ```

  ```js
  // Map the searched painting to its original index and set this as the clickID for the rest of the program
  function searchPainting(searchedPainting, indexList) {
    if (searchedPainting == "") {
      return null;
    } else {
      let searchIndex = indexList.indexOf(searchedPainting);
      return searchIndex;
    }
  }

  setClickId(searchPainting(paintingSearch, titleIdArray));
  const clickArray = [];
  ```

  <h3>Painting timeline options</h3>

  ```js
  // A button to add a clicked painting to a painting subset
  let clickArrayContainerContent = document.querySelector("#clickArrayContainer");

  function displayClickArray(paintingData, clickedArray) {
    if (clickedArray.length == 0) {
      clickArrayContainerContent.innerHTML = `
      Select paintings for the subset by clicking the <br> painting and confirming with the button
      `;
    } else {
      const displayArray = [];
      for (let i=0; i<clickedArray.length; i++) {
        if (!displayArray.includes(paintingData[Number(clickedArray[i])].fnumber) && typeof clickedArray[i] != "number") {
          displayArray.push(paintingData[Number(clickedArray[i])].fnumber);
        }
      }
      
      clickArrayContainerContent.innerHTML = `
      Paintings in the subset: ${displayArray}
      `;
    }
  }

  // These two lines should stay in the same code block otherwise the subset clicks will break :3
  paintingSubset;
  displayClickArray(paintingsImages, clickArray);
  ```

  ```js
  // Create radio boxes for timeline layout
  const selection = view(Inputs.radio(["Time points - Start", "Time points - Middle", "Time points - End", "Time ranges"], {label: "Choose timeline", value: "Time points - Middle"}));
  ```

  ```js
  const nrows = (Math.max(...lanesData(paintingsAnalyzed).map(o => o.yIndex))) + 1;
  const n = (nrows < 50) ? 25 : 50;

  // Allow for the slider to be disabled when the time ranges option is clicked (then radius does not apply)
  const disabledSlider = [];
  if (selection === "Time ranges") {
    disabledSlider.push(true);
  } else { 
    disabledChoice.push(false);
  };

  // Create a slider to adjust radius of time points
  const radiusSize = view(Inputs.range([0, 25], {label: "Set point radius", step: 0.5, value: 650 / (nrows + n), disabled: disabledSlider[0]}));
  ```

  ```js
  // Create radio buttons for selecting the paintings that are displayed based on the "analyzed" feature
  const analyzedChoice = view(Inputs.radio(["All paintings", "Analyzed paintings", "Not analyzed paintings"], 
  {label: "Pigment analysis filter", value: "All paintings"}));
  ```

  <h3>Pigment overview options</h3>

  ```js
  // Create radio buttons for choosing the pigment display
  const pigmentRadio = view(Inputs.radio(new Map([["Pigments", "pigment"], ["Colorgroups", "Colorgroup"]]), {label: "Choose display", value: "pigment"}));
  ```

  ```js
  const pigmentNames = d3.groupSort(pigment_counts, 
      ([d]) => d.Colorgroup,
      (d) => d.pigment
    );
  const colorgroupNames = extractNames(pigment_counts, 'Colorgroup');
  ```

  ```js
  const disabledChoice = [];
  if (pigmentRadio === "pigment") {
    disabledChoice.push(false)
  };
  if (pigmentRadio === "Colorgroup") {
    disabledChoice.push(true)
  };

  // Create a selection pane to filter on pigment name (disabled when the color group option is selected!)
  let pigmentSelect = [];
  pigmentSelect = view(Inputs.select(pigmentNames, {disabled: disabledChoice[0], multiple: true, label: "Choose pigment(s)"}));

  display(Inputs.button("Reset pigment selection (clicked painting)", {reduce: () => setPigmentClicked([])}));
  ```

  ```js  
  // Only show options for technique that are present in the current pigment data selection
  const techniqueOptions = [];

  for (let i=0; i<pigment_counts.length; i++) {
    if (pigment_counts[i].technique != null && pigment_counts[i].technique.length > 0) {
      for (let j=0; j<pigment_counts[i].technique.length; j++) {
        if (!techniqueOptions.includes(pigment_counts[i].technique[j])) {
          techniqueOptions.push(pigment_counts[i].technique[j]);
        }
      }
    } else {
      if (!techniqueOptions.includes("No info")) {
        techniqueOptions.push("No info");
      }
    }
  }

  // Create checkboxes for filtering pigments on the technique
  const techniqueChoice = view(Inputs.checkbox(techniqueOptions, {label: "Choose technique(s)", value: techniqueOptions}));
  ```

  ```js
  // Create checkboxes for filtering pigments on the uncertainty
  const uncertaintyChoice = view(Inputs.checkbox(["No info", "Possibly", "Probably"], {label: "Choose uncertainty", value: ["No info", "Possibly", "Probably"]}));
  ```

  ```js
  // The code in the following blocks generates the painting details view

  let containerContent = document.querySelector('#container');
  const full_month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  function paintingView(paintingData, clickedId = null) {

    if (clickedId == null) {
      containerContent.innerHTML = `
      <br>
      <h3>Painting details - Click on a painting to display more details here</h3>
      `;
    } else {
      const clickedPainting = paintingData[Number(clickedId)];

      // Create a list of letterIDs with correct associated URLs
      let letterArray = [];
      for (let i = 0; i < clickedPainting.letterIDs.length; i++) {
        if (clickedPainting.letterIDs[i] == null) {
          letterArray.push(null);
        } else {
          letterArray.push("<a href='" + clickedPainting.letterURLs[i] + "' target='_blank'>" + clickedPainting.letterIDs[i] + "</a>");
        }
      }
      
      containerContent.innerHTML = `
        <br>
        <h3>Painting details - ${clickedPainting.title}</h3>
        <a href=${clickedPainting.link} target="_blank">Van Gogh Worldwide page</a>
        <table><tr>
          <td>F-number</td>
          <td id="clickedF">${clickedPainting.fnumber}</td>
        </tr><tr>
          <td>JH-number</td>
          <td>${clickedPainting.jhnumber}</td>
        </tr><tr>
          <td>Museum ID</td>
          <td>${clickedPainting.museum_id}</td>
        </tr><tr>
          <td>Date</td>
          <td>${clickedPainting.display}</td>
        </tr><tr>
          <td>Production location</td>
          <td>${clickedPainting.location}</td>
        </tr><tr>
          <td>Current owner</td>
          <td>${clickedPainting.current_owner}</td>
        </tr><tr>
          <td>Pigment analysis?</td>
          <td>${clickedPainting.analyzed}</td>
        </tr><tr>
          <td>Associated letter(s)</td>
          <td>${letterArray}</td>
        </tr></table>

        <img id="clickedImage" src=${clickedPainting.image}>
        `;
    }
  }

  paintingView(paintingsImages, clickId);
  ```

  ```js
  // Function to fill the pigmentChoice array with pigments based on the clicked painting
  function pigmentClick(paintingData, pigmentData, clickedId) {
    
    const clickedPainting = paintingData[Number(clickedId)];
    const resultArray = [];

    if (clickedId == null) {
      return [];
    } else if (clickedPainting.analyzed == "No") {
      return ["placeholder"];
    } else {
      for (let i=0; i < pigmentData.length; i++) {
        if (pigmentData[i].fnumber == clickedPainting.fnumber) {
          resultArray.push(pigmentData[i].pigment);
        }
      }
      return resultArray;
    } 
  } 

  setPigmentClicked(pigmentClick(paintingsImages, pigment_counts, clickId));
  ```
  <div class="container" id="container"></div>

  ```js

  let containerTable = document.querySelector('#container2');
  // Function to set the pigment table at the bottom of the painting details view
  function pigmentTable(paintingData, pigmentData, clickedId = null) {
    
    if (clickedId == null) {
      containerTable.innerHTML = ``;
    } else {
      const clickedPainting = paintingData[Number(clickedId)];
      
      if (clickedPainting.analyzed == "No"){
        containerTable.innerHTML = `
        <br>
        <h3>No pigment data to display</h3>
        `;
      } else {
        let clickedPigments = pigmentData.filter(function(el) {
          return el.fnumber == clickedPainting.fnumber;
        });

        // A map to display the encoded source as a nicely written source
        const sourceMap = new Map([
          ["dutch_table", "Van Gogh's Dutch Palette - Van Gogh's Studio Practice by M. Geldof, L. Megens, and J. Salvant (2013)"],
          ["antwerp_table", "Vincent van Gogh Paintings: Volume 2: Antwerp, Paris 1885-1888 by E. Hendriks and L. van Tilborgh (2011)"], 
          ["paris_table", "Vincent van Gogh Paintings: Volume 2: Antwerp, Paris 1885-1888 by E. Hendriks and L. van Tilborgh (2011)"],
          ["olive_table", "Creating Olive Groves in Saint-Rémy: A Comparative Study of Van Gogh's Painting Technique and Materials - Van Gogh and the Olive Groves by K. Pilz and M. Geldof (2021)"],
          ["astra_table", "Van Gogh's Palette in Arles, Saint-Rémy and Auvers-Sur-Oise - Van Gogh's Studio Practice by M. Geldof, L. Megens, and J. Salvant (2013)"]
        ]);

        // Ensure the display order of pigments in the table is the same as in the pigment dots plot
        let sortedPigmentNames = d3.groupSort(clickedPigments, ([d]) => d.Colorgroup, (d) => d.pigment);
        
        function mapOrder(array, order, key) {
          array.sort(function(a, b) {
            let A = a[key], B = b[key];

            if (order.indexOf(A) > order.indexOf(B)) {
              return 1;
            } else {
              return -1;
            }
          });

          return array;
        };

        const sortedPigments = mapOrder(clickedPigments, sortedPigmentNames, "pigment");

        const pigmentsTable = Inputs.table(sortedPigments, {
          columns: [
            "pigment",
            "certainty",
            "technique",
            "notes"
          ],
          header: {
            pigment: "🎨",
            certainty: "❔",
            technique: "🔎",
            notes: "📝"
          },
          layout: "auto",
          rows: 25
        });

        containerTable.innerHTML = `
        <br>
        <i>Pigment analysis source:</i> ${sourceMap.get(clickedPigments[0].source)}
        <br>
        <br>
        `;
        containerTable.appendChild(pigmentsTable);
      };
    };
  };
  
  pigmentTable(paintingsImages, pigment_counts, clickId);
  ```
  <div class="container2" id="container2"></div>

  </div>
  <div class="grid-colspan-3">
  
  ```js
  // Data imports
  const paintingsRawImages = FileAttachment("./data/painting_data_full_images.json").json();
  // const paintingsRawImages = FileAttachment("./data/paintingdlf_data_full_images.json").json();
  const pigment_counts_raw = FileAttachment("./data/vgm_pigment_counts.json").json();
  const counts = FileAttachment("./data/vgm_paintings_real_letter_counts.json").json();
  const periods_raw = FileAttachment("./data/period_data.json").json();
  ```

  ```js
  // Package imports
  import d3Tip from "d3-tip";
  import tippy from "tippy.js"; 
  ```

  ```js
  // The code in the blocks below is used to build the period overview timeline in the standard timelines

  function parsePeriods(element) {
    return {
      period: element.period,
      start: new Date(element.start),
      end: new Date(element.end),
      middle: new Date(new Date(element.start).getTime() + (new Date(element.end).getTime() - new Date(element.start).getTime()) / 2),
      locations: element.locations, 
      background: element.background
    }
  };

  const periods = periods_raw.map(parsePeriods);
  ```

  ```js
  // Creates a subset of periods based on the location of the clicked painting
  function clickedPeriod(paintingData, periodData, clickedId = null) {
    
    if (clickedId == null) {
      return [];
    } else {
      const clickedPainting = paintingData[Number(clickedId)];
      const periodOut = [];
      
      for (let i=0; i<periodData.length; i++) {
        if (periodData[i].locations.includes(clickedPainting.location)) {
          periodOut.push(periodData[i].period);
        } 
      }
      return periodOut;
    }
  }
  ```

  ```js
  let periodSubset = clickedPeriod(paintingsImages, periods, clickId);
  if (periodSubset.length == 0) {
    periodSubset = periods.map((d) => d.period);
  }
  
  // Create the actual plot
  display(
    Plot.plot({
      height: 100,
      width: width, 
      marginLeft: 150,
      x: {domain: [new Date("1881-01-01"), new Date("1891-01-01")]}, 
      y: {domain: [0, 1], axis: null},
      marks: [
        Plot.ruleY([0]),
        Plot.axisX({label: null, fontSize: 15}),
        Plot.image(periods, {
          x: "middle", 
          y: 0.5, 
          src: "background",
          height: 50,
          width: d => 
          (d.start >= d.end
            ? 3
            : xScale(d.end) - xScale(d.start)
          ),
          preserveAspectRatio: "none",
          channels: {
            start: {
              value: "start",
              label: "Start"
            },
            end: {
              value: "end",
              label: "End"
            }
          },
          tip: {
            fontSize: 15,
            format: {
              x: false,
              y: false,
              width: false,
              start: true,
              end: true
            }
          }
        }), 
        Plot.text(periods, {
          x: "middle", 
          y: [0.5, 1, 0.5, 0.5, 0.5, 0.5, 1], 
          text: "period", 
          fontSize: 20,
          opacity: (d) => (
            periodSubset.includes(d.period) ? 1 : 0.3
          ),
        })
      ]
    })
  )
  ```

  ```js
  // The code block below build the letter and painting counts bar chart from the standard timelines
  display(
      Plot.plot({
          style: {fontSize: "15px"},
          x: {axis: null, tickFormat: "%Y", label: null},
          fx: {label: null},
          y: {tickFormat: "s", grid: true, label: "Count"},
          width: width,
          height: 100, 
          marginLeft: 150, 
          color: {type: "categorical", range: ["#00abff", "#ffa420"], legend: true},
          marks: [
              Plot.barY(counts, {
                  x: "key",
                  y: "count",
                  fill: "key",
                  fx: "year",
                  channels: {
                    count: {
                      value: "count", 
                      label: "Count"
                    }, 
                    year: {
                      value: "year",
                      label: "Year"
                    }, 
                    key: {
                      value: "key", 
                      label: "Data"
                    }
                  },
                  tip: {
                    fontSize: 15, 
                    format: {
                      x: false, 
                      y: false, 
                      fill: false,
                      fx: false
                    }
                  }
              }),
              Plot.ruleY([0])
          ]
      })
  );
  ```
  <div class="clickArrayContainer" id="clickArrayContainer"></div>

  ```js
  // The code blocks below are used to build the painting timeline

  // Create the painting subset menu with options
  const paintingSubset = view(Inputs.button([
    [html`Add ${paintingsImages[Number(clickId)].fnumber} to subset`, value => clickArray.push(value)],
    ["Show pigment overlap for subset", () => setPigmentClicked(setSubsetPigments(paintingsImages, pigment_counts, clickArray))],
    ["Reset pigment subset", () => clickArray.length = 0]
  ], {value: clickId}));
  ```

  ```js
  // Function to set the pigments overview based on the paintings selected in the subset
  function setSubsetPigments(paintingData, pigmentData, subsetArray) {

    const resultArray = [];
    const placeholderArray = [];
    const counter = {};

    if (subsetArray.length == 0) {
      return [];
    } else if (subsetArray.length == 1) {
      const firstPaintingArray = pigmentClick(paintingData, pigmentData, subsetArray[0]);
      return firstPaintingArray;
    } else {
      const subsetArrayUnique = [...new Set(subsetArray)];
      const subsetArrayFinal = subsetArrayUnique.filter(item => typeof item === "string");

      for (let i=0; i<subsetArrayFinal.length; i++) {
        if (typeof subsetArrayFinal[i] == "string") {
          let singlePaintingArray = pigmentClick(paintingData, pigmentData, subsetArrayFinal[i]);
          for (let j=0; j<singlePaintingArray.length; j++) {
            placeholderArray.push(singlePaintingArray[j]);
          }
        }
      }

      // Compute how many times each pigment has been added
      // Only pigments that have been added as many times as subsetArray is long, will be considered for the final result
      placeholderArray.forEach(el => {
        if (counter[el]) {
          counter[el] += 1;
        } else {
          counter[el] = 1;
        }
      });
      
      for (const [key, value] of Object.entries(counter)) {
        if (value === subsetArrayFinal.length) {
          resultArray.push(key);
        }
      }
      return resultArray;
    }
  }
  ```

  ```js
  // Necessary functions for the painting timelines: stacking algorithm and data parser
  const lanesData = data => {
    const lanesData = []
    let stack = [];
    data.slice().forEach(e => {
      const lane = stack.findIndex(
        s => s[END_YEAR] <= e[START_YEAR] && s[START_YEAR] < e[START_YEAR]
        // s => s[END_YEAR] < e[START_YEAR] || e[END_YEAR] < s[START_YEAR]
      );
      const yIndex = lane === -1 ? stack.length : lane
      lanesData.push({
        ...e,
        yIndex
      })
      stack[yIndex] = e;
    })
    return lanesData
  }

  const START_YEAR = "start";
  const END_YEAR = "end";

  // Be careful when filtering: make sure the new dataset always passes through this function (or make a separate function for the sorting + index assignment!)
  function parseDates(data) {
    const parsedArray = [];
    for (let i = 0; i < data.length; i++) {
      const element = data[i];
      parsedArray.push({
        start: new Date(element.start),
        end: new Date(element.end),
        middle: new Date(new Date(element.start).getTime() + (new Date(element.end).getTime() - new Date(element.start).getTime()) / 2),
        display: element.display,
        title: element.title,
        image: element.Image, 
        fnumber: element.fnumber,
        jhnumber: element.jhnumber,
        museum_id: element.museumid,
        location: element.location,
        current_owner: element.current_owner,
        link: element.link,
        analyzed: element.analyzed,
        letterIDs: element.letterID,
        letterURLs: element.letterURL});
    }
    
    const sortedArray = parsedArray.sort(
      (a, b) => 
      d3.ascending(a[START_YEAR], b[START_YEAR]) ||
      d3.ascending(a[END_YEAR], b[END_YEAR])
    );

    // Index assignment for quicker data loading
    for (let i = 0; i < data.length; i++) {
      sortedArray[i].index = i.toString();
    };

    return sortedArray;
  };

  const paintingsImages = parseDates(paintingsRawImages)
  // For now change the index of the second F25 manually to make it match the first
  paintingsImages[41].index = 6;

  // A filtered dataset based on the pigment analysis radio choice
  let paintingsAnalyzed;
  if (analyzedChoice == "Analyzed paintings") {
    paintingsAnalyzed = paintingsImages.filter(item => item.analyzed == "Yes");
  } else if (analyzedChoice == "Not analyzed paintings") {
    paintingsAnalyzed = paintingsImages.filter(item => item.analyzed == "No");
  } else {
    paintingsAnalyzed = paintingsImages;
  }

  const month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

  const placedPaintings = lanesData(paintingsImages); // I think this line is redundant?
  ```

  ```js
  // Function that accepts a painting index and generates the html tooltip accordingly
  function tip(id) {
    let d = paintingsImages.filter((c) => c.index == id)[0];
    return `<h4>${d.title} (${d.fnumber})</h4>
    ${d.location}
    <br> ${d.display}
    <br> <img src=${d.image} width="200">
    `;
  }
  ```
  ```js
  // Code to create an f-array to pass to the opacity option in the timeline plots
  const fArray = [];

  if (Array.isArray(pigmentDot)) {
    for (let i = 0; i < pigmentDot.length; i++) {
      fArray.push(pigmentDot[i].fnumber);
    }
  }

  // If the f-array is empty, pass all f-numbers in the current set to ensure opacity is 1 in 'rest'
  // (otherwise, just keep the f-array as is)
  if (fArray.length === 0) {
    for (let i = 0; i < paintingsImages.length; i++) {
      fArray.push(paintingsImages[i].fnumber);
    }
  }
  ```

  ```js
  const clickId = Mutable(null);
  const setClickId = (value) => clickId.value = value;

  const pigmentClicked = Mutable([]);
  const setPigmentClicked = (value) => pigmentClicked.value = value;
  ```

  ```js
  // Painting timelines: point and range based
  const xScale = d3
      .scaleTime()
      .domain([new Date("1881-01-01"), new Date("1890-01-01")])
      .nice()
      .range([40, width - 15]);

  const maxHeight = 600;  
  const zeroArray = new Array(paintingsAnalyzed.length).fill(0);

  function points_timeline(paintingData, position, subset) {
    let points_timeline = Plot.plot({
      height: maxHeight,
      width: width,
      marginLeft: 150,
      x: {domain: [new Date("1881-01-01"), new Date("1891-01-01")]},
      color: {
        range: ["white", "white"]
      },
      marks: [
        Plot.axisX({label: null, fontSize: 15}),
        Plot.image(
          paintingData,
          Plot.dodgeY({
            x: position, 
            r: radiusSize,
            padding: -0.5,
            opacity: (d) => (
                subset.includes(d.fnumber) ? 1 : 0.3
              ),
            preserveAspectRatio: "xMidYMind slice",
            src: "image",
            title: "index",
          })
        ),
        Plot.dotX(
          paintingData,
          Plot.dodgeY({
            x: position,
            r: radiusSize,
            padding: -0.5,
            fill: "black",
            fillOpacity: zeroArray,
            title: "index"
          })
        )
      ]
    });
    
    let boxDots = d3.select(points_timeline).selectAll("circle");
    boxDots
      .on("click", function() {
        let t = d3.select(this).select("title").text();
        setClickId(t);
      })
      .each(function () {
        let t = d3.select(this).select("title").text(); 
        tippy(this, {
          content: tip(t),
          theme: 'custom',
          allowHTML: true,
          maxWidth: 200,
          interactive: true,
          appendTo: () => document.body
        })
      })
      .each(function () {
        let t = d3.select(this).select("title").text();
        if (t == clickId) {
          d3.select(this).attr("stroke", "red").style("stroke-width", 4);
        }
      })
    
    return points_timeline;
  }

  function range_timeline(paintingData, subset) {
    let range_timeline = Plot.plot({
      height: maxHeight,
      width: width,
      marginLeft: 150,
      x: {domain: [new Date("1881-01-01"), new Date("1891-01-01")]},
      y: {domain: [0, nrows], axis: null},
      marks: [
        Plot.axisX({label: null, fontSize: 15}),
        Plot.image(lanesData(paintingData), {
          x: "middle",
          y: d => (d.yIndex + 0.5), 
          src: "image",
          height: maxHeight / nrows,
          width: d =>
          (d.start >= d.end
            ? 3
            : xScale(d.end) - xScale(d.start)),
          opacity: (d) => (
                subset.includes(d.fnumber) ? 1 : 0.3
              ),
          preserveAspectRatio: "none",
          title: "index"

        })
      ]
    })

    const borderId = "outline";
    const borderRadius = 5;
    const borderStroke = "red";

    let paintings = d3.select(range_timeline).selectAll("image");
    paintings
      .on("click", function() {
        let t = d3.select(this).select("title").text();
        setClickId(t);
      })
      .each(function () {
        let t = d3.select(this).select("title").text(); 
        tippy(this, {
          content: tip(t),
          theme: 'custom',
          allowHTML: true,
          maxWidth: 200,
          interactive: true,
          appendTo: () => document.body
        })
      })
      .each(function () {
        let t = d3.select(this).select("title").text();
        if (t == clickId) {
          d3.select(this).attr("filter", `url(#${borderId})`);
        }
      })

      d3.select(range_timeline).append("defs").html(`<filter id="${borderId}">
        <feMorphology in="SourceAlpha" result="expanded" operator="dilate" radius="${borderRadius}"/>
        <feFlood flood-color="${borderStroke}"/>
        <feComposite in2="expanded" operator="in"/>
        <feComposite in="SourceGraphic"/>
      </filter>`);
    
    return range_timeline;
  }
  ```

  ```js
  // Function to display the plot chosen with the radio boxes above
  function makeTimeline(selection) {
    let plot;
    if (selection === "Time points - Start") {
      plot = points_timeline(paintingsAnalyzed, "start", fArray);
    } else if (selection === "Time points - Middle") {
      plot = points_timeline(paintingsAnalyzed, "middle", fArray);
    } else if (selection === "Time points - End") {
      plot = points_timeline(paintingsAnalyzed, "end", fArray);
    } else {
      plot = range_timeline(paintingsAnalyzed, fArray);
    }

    return plot
  };

  display(makeTimeline(selection));
  ```

  ```js
  // The code blocks below are used to build the pigment overview timeline

  // Function for pigment data parsing
  function parseYears(element) {
      return {
          pigment: element.pigment,
          yearMiddle: new Date(new Date(element.year).setMonth(new Date(element.year).getMonth()+6)),
          year: element.year,
          Colorgroup: element.colorgroup,
          fnumber: element.painting,
          details: element.details,
          source: element.source,
          certainty: element.uncertainty,
          technique: element.technique,
          notes: element.notes
      }
  };

  const pigment_counts = pigment_counts_raw.map(parseYears);
  ```

  ```js
  let pigmentChoice = [];
  if (pigmentSelect.length > 0) {
    pigmentChoice = pigmentSelect;
  } else if (pigmentClicked.length > 0 && pigmentSelect.length == 0) {
    pigmentChoice = pigmentClicked;
  }
  ```

  ```js
  // Pigment overview plot
  const pigment_counts_filtered = [];

  if (pigmentChoice.length > 0) {
    for (let i = 0; i < pigment_counts.length; i++) {
      if (pigmentChoice.includes(pigment_counts[i]["pigment"])) {
        pigment_counts_filtered.push(pigment_counts[i]);
      }
    }
  }
  const filteredInput = (pigmentChoice.length <= 0) ? pigment_counts : pigment_counts_filtered;

  const finalInput = [];
  // Select from filteredInput based on the chosen techniques and uncertainty
  for (let i=0; i<filteredInput.length; i++) {
    let technique = filteredInput[i].technique;
    let uncertainty = filteredInput[i].certainty;

    // Case 1 where both technique and certainty are null
    if (technique == null && uncertainty == null && techniqueChoice.includes("No info") && uncertaintyChoice.includes("No info")) {
      finalInput.push(filteredInput[i]);
    }

    // Case 2 where technique is null and the certainty is a string
    if (technique == null && uncertainty != null && techniqueChoice.includes("No info") && uncertaintyChoice.includes(uncertainty)) {
      finalInput.push(filteredInput[i]);
    }

    // Case 3 where technique is an array and the certainty is a string
    if (technique != null && uncertainty != null) {
      if (technique.length == 0) {
        if (techniqueChoice.includes("No info") && uncertaintyChoice.includes(uncertainty)) {
          finalInput.push(filteredInput[i]);
        } 
      } else {
        for (let j=0; j<technique.length; j++) {
          if (techniqueChoice.includes(technique[j]) && uncertaintyChoice.includes(uncertainty) && !finalInput.includes(filteredInput[i])) {
            finalInput.push(filteredInput[i]);
          }
        }
      }
    }

    // Case 4 where technique is an array and the uncertainty is null
    if (technique != null && uncertainty == null) {
      if (technique.length == 0) {
        if (techniqueChoice.includes("No info") && uncertaintyChoice.includes("No info")) {
          finalInput.push(filteredInput[i]);
        }
      } else {
        for (let j=0; j<technique.length; j++) {
          if (techniqueChoice.includes(technique[j]) && uncertaintyChoice.includes("No info") && !finalInput.includes(filteredInput[i])) {
            finalInput.push(filteredInput[i]);
          }
        }
      }
    }
  }

  const yDomain = (pigmentRadio === "pigment") ? d3.groupSort(
      finalInput, 
      ([d]) => d.Colorgroup,
      (d) => d.pigment
    ) : colorgroupNames;

  const pigmentHeight = (pigmentChoice.length > 0) ? 40*pigmentChoice.length : 25*pigmentNames.length;

  const plotHeight = (pigmentRadio === "pigment") ? pigmentHeight : 40*colorgroupNames.length;

  const minHeight = (plotHeight > 160) ? plotHeight : 160;

  const pigmentDot = view(Plot.plot({
    label: null, 
    marginLeft: 150,
    height: minHeight,
    width: width,
    grid: true,
    x: {domain: [new Date("1881-01-01"), new Date("1891-01-01")], label: "Year"},
    y: {domain: yDomain, label: "Pigment"},
    r: {range: [0, 20], label: "Absolute count"},
    marks: [
      Plot.axisY({anchor: "left", tickRotate: 0, fontSize: 15, label: null}),
      Plot.axisX({fontSize: 15, label: null}),
      Plot.dot(finalInput, 
      Plot.group({
        r: "count"
      },
      {
        x: "yearMiddle", 
        y: pigmentRadio, 
        stroke: "black",
        fill: "Colorgroup",
        fillOpacity: 0.5,
        tip: {
          fontSize: 15,
          format: {
            x: (d) => `${d.getFullYear()}`, 
            stroke: false
          }
        }
      }
    ))
    ]
  })
  )
  ```

  ```js
  //Function to extract the unique pigments and colorgroups from the counts and store in an array
  function extractNames(data, groupName) {
    const result = [];
    const lookup = [];

    for (let i = 0; i < data.length; i++) {
        let name = data[i][groupName]

        if (!(name in lookup)) {
          lookup[name] = 1;
          result.push(name);
        }
    }

    return result.sort()
  }
  ```
  
  </div>
</div>


