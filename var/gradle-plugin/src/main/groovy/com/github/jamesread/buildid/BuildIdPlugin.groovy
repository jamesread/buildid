package com.github.jamesread.buildid

import org.gradle.api.Project
import org.gradle.api.Plugin
import org.gradle.api.tasks.Exec;
import java.lang.ProcessBuilder;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors

class BuildIdPlugin implements Plugin<Project> {
	String message = "?";

	void apply(Project project) {
		project.extensions.create("buildid", BuildIdImpl)

		project.task("greeting") {
			doLast {
				println "buildid: ${project.buildid.message}"
			}
		}
	}
}

class BuildIdImpl {
	private void exec(String cmdline) {
		ProcessBuilder processBuilder = new ProcessBuilder(cmdline.split(" "));
		Process process = processBuilder.start();
		process.waitFor()

		String output = new BufferedReader(new InputStreamReader(process.getInputStream())).lines().collect(Collectors.joining("\n"));

		println(output);
	}

	Properties newBuild() {
		this.exec("buildid -n");

		return readProperties();
	}

	void writeRpmMacro() {
		this.exec("buildid -qf rpmmacro -W .buildid.rpmmacro")
	}

	void writeIni() {
		this.exec("buildid -qf rpmmacro -W .buildid.ini")
	}

	Properties read() {
		return readProperties()
	}

	Properties readProperties() {
		Properties props = new Properties()
		props.load(new File(".buildid").newReader())

		return props
	}

	String get(String key) {
		return read().get(key)
	}
}
