// 4/18/2024 The program in this file is the individual work of Preston Byk Hanako21
let date = new Date();
let fullYear = date.getFullYear();

function renderCalendar() {
  date.setDate(1);

  const monthDays = document.getElementById("dates");
  const month = document.getElementById("month");
  const daysElement = document.getElementById("days");
  const prev = document.getElementById("prev");

  let months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  let lastDay = new Date(fullYear, date.getMonth() + 1, 0).getDate();
  let prevLastDay = new Date(fullYear, date.getMonth(), 0).getDate();
  let firstDayIndex = new Date(fullYear, date.getMonth(), 0).getDay() + 1;

  let monthStr = months[new Date().getMonth()]; // get month as a string
  let year = date.getFullYear();

  if (parseInt(month.value) == -2) {
    month.value = 0;
  }

  if (month.value >= 0) {
    lastDay = new Date(fullYear, parseInt(month.value) + 1, 0).getDate();
    prevLastDay = new Date(fullYear, parseInt(month.value), 0).getDate();
    firstDayIndex = new Date(fullYear, parseInt(month.value), 0).getDay() + 1;
    monthStr = months[parseInt(month.value)];
  }

  lastDayIndex = new Date(fullYear, parseInt(month.value) + 1, 0).getDay();

  const formattedDate = `${monthStr} ${year}`;
  month.value = formattedDate;

  const nextDays = 6 - lastDayIndex;

  const days = ["S", "M", "T", "W", "T", "F", "S"];

  daysElement.innerHTML = days.map((day) => `<div>${day}</div>`).join("");

  let dates = "";

  for (let i = firstDayIndex; i > 0; i--)
    dates += `<div class='prev-date'>${prevLastDay - i + 1}</div>`;

  for (let i = 1; i <= lastDay; i++) {
    if (i == new Date().getDate() && date.getMonth() == new Date().getMonth())
      dates += `<div class='today'>${i}</div>`;
    else dates += `<div>${i}</div>`;
  }

  for (let i = 1; i <= nextDays; i++)
    dates += `<div class='next-date'>${i}</div>`;

  monthDays.innerHTML = dates;
}

renderCalendar();
