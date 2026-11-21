export type NameParts = {
  first_name: string;
  last_name?: string | null;
};

export type TrainerHeading = NameParts & {
  photo: string | null;
};

export function clientName(client: NameParts) {
  const lastName = client.last_name?.trim() ?? "";
  if (!lastName) {
    return client.first_name;
  }
  return `${lastName} ${client.first_name}`;
}

export function trainerMark(trainer: TrainerHeading) {
  if (trainer.photo) {
    return { kind: "photo" as const, url: trainer.photo };
  }
  const letters = [trainer.first_name, trainer.last_name ?? ""].map((part) => part.trim().charAt(0)).filter(Boolean);
  return { kind: "initials" as const, text: letters.join("").toLocaleUpperCase("ru") };
}

function sortKey(client: NameParts) {
  const lastName = client.last_name?.trim();
  if (lastName) {
    return `${lastName}\u0000${client.first_name}`;
  }
  return client.first_name;
}

export function visibleClients<T extends NameParts>(clients: T[], query: string) {
  const needle = query.trim().toLocaleLowerCase("ru");
  const matched = needle
    ? clients.filter((client) => {
        const haystack = `${client.last_name ?? ""} ${client.first_name}`.toLocaleLowerCase("ru");
        return haystack.includes(needle);
      })
    : clients.slice();
  return matched.sort((left, right) => sortKey(left).localeCompare(sortKey(right), "ru"));
}

export function clientCountLabel(count: number) {
  const mod10 = count % 10;
  const mod100 = count % 100;
  if (mod10 === 1 && mod100 !== 11) {
    return `${count} клиент`;
  }
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) {
    return `${count} клиента`;
  }
  return `${count} клиентов`;
}
