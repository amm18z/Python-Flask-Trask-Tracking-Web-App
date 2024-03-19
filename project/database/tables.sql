USE TaskTracker;

CREATE TABLE IF NOT EXISTS `TaskTracker`.`Tasks` (
  `id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `descr` VARCHAR(45) NULL,
  `creation_date` DATE NULL,
  `due_date` DATE NULL,
  `priority` INT NULL,
  UNIQUE INDEX `idTasks_UNIQUE` (`id` ASC) VISIBLE,
  PRIMARY KEY (`id`));
  
CREATE TABLE IF NOT EXISTS `TaskTracker`.`Users` (
  `id` INT NOT NULL,
  `password` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `password_UNIQUE` (`password` ASC) VISIBLE);
  
CREATE TABLE IF NOT EXISTS `TaskTracker`.`Assignments` (
  `id` INT NOT NULL,
  `Users_id` INT NOT NULL,
  `Tasks_id` INT NOT NULL,
  PRIMARY KEY (`id`, `Users_id`, `Tasks_id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_Assignments_Users_idx` (`Users_id` ASC) VISIBLE,
  INDEX `fk_Assignments_Tasks1_idx` (`Tasks_id` ASC) VISIBLE,
  CONSTRAINT `fk_Assignments_Users`
    FOREIGN KEY (`Users_id`)
    REFERENCES `TaskTracker`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Assignments_Tasks1`
    FOREIGN KEY (`Tasks_id`)
    REFERENCES `TaskTracker`.`Tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
    
show tables;