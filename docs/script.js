const demos = {
  time: {
    user: "What time is it right now in America/Phoenix?",
    reason: "The request needs fresh time data, so the graph should call the time tool.",
    act: 'get_current_time({"timezone_name":"America/Phoenix"})',
    observe: "The tool returns a formatted local timestamp from Python's zoneinfo database.",
    answer: "It is the current time in America/Phoenix, returned from the tool observation.",
  },
  count: {
    user: 'How many words are in "the quick brown fox jumps"?',
    reason: "The request maps directly to the word_count tool.",
    act: 'word_count({"text":"the quick brown fox jumps"})',
    observe: "The tool counts five words.",
    answer: "There are 5 words.",
  },
  explain: {
    user: "Explain the ReAct pattern in two sentences.",
    reason: "No external tool is needed; the model can answer from its own context.",
    act: "No tool call.",
    observe: "The graph keeps the conversation state and proceeds to the final response.",
    answer:
      "ReAct alternates between reasoning about the next step and acting through tools. The observation from each action helps the model produce a grounded answer.",
  },
};

const ids = ["user", "reason", "act", "observe", "answer"];

function renderDemo(name) {
  const demo = demos[name] || demos.time;
  ids.forEach((id) => {
    const target = document.getElementById(`trace-${id}`);
    if (target) {
      target.textContent = demo[id];
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderDemo("time");

  document.querySelectorAll(".query-button").forEach((button) => {
    button.addEventListener("click", () => {
      document
        .querySelectorAll(".query-button")
        .forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      renderDemo(button.dataset.demo);
    });
  });

  if (window.lucide) {
    window.lucide.createIcons();
  }
});
