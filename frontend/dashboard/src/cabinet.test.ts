import { describe, expect, it } from "vitest";

import { clientCountLabel, clientName, trainerMark, visibleClients } from "./cabinet";

const clients = [
  { id: 1, first_name: "Анна", last_name: "Козлова" },
  { id: 2, first_name: "Пётр", last_name: "" },
  { id: 3, first_name: "Елена", last_name: "Волкова" },
];

describe("cabinet", () => {
  it("показывает фамилию и имя", () => {
    expect(clientName(clients[0])).toBe("Козлова Анна");
  });

  it("без фамилии показывает имя", () => {
    expect(clientName(clients[1])).toBe("Пётр");
  });

  it("сужает список по фрагменту имени", () => {
    expect(visibleClients(clients, "коз").map((client) => client.id)).toEqual([1]);
  });

  it("без поиска показывает всех по алфавиту и считает строки", () => {
    const shown = visibleClients(clients, "  ");
    expect(shown.map((client) => client.id)).toEqual([3, 1, 2]);
    expect(shown).toHaveLength(3);
    expect(clientCountLabel(shown.length)).toBe("3 клиента");
  });

  it("без фото показывает инициалы", () => {
    expect(trainerMark({ first_name: "Иван", last_name: "Петров", photo: null })).toEqual({
      kind: "initials",
      text: "ИП",
    });
  });

  it("с фото показывает адрес", () => {
    expect(trainerMark({ first_name: "Иван", last_name: "Петров", photo: "https://photos/face.jpg" })).toEqual({
      kind: "photo",
      url: "https://photos/face.jpg",
    });
  });
});
